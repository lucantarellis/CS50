from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helper import login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///local-store.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
@login_required
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    if request.method == "POST":
        # Ensure username and password where inputed
        username = request.form.get("username")
        if not username:
            flash("Must provide an username")
            role = "alert-danger"
            return render_template("login.html", role=role)

        password = request.form.get("password")
        if not password:
            flash("Must provide a password")
            role = "alert-danger"
            return render_template("login.html", role=role)

        # Query db to know if username + password exist and are correct
        rows = db.execute("SELECT * FROM users WHERE username = (?)", username)
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            flash("Invalid username and/or password")
            role = "alert-danger"
            return render_template("login.html", role=role)

        # Remember user
        session["user_id"] = rows[0]["id"]

        # Send user to home page
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    # Forget user_id
    session.clear()

    # Redirect user to login
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Retrieve email and password from inputs
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")

        # Check info is correct
        if not username:
            flash("Must provide an username to create an account")
            role = "alert-danger"
            return render_template("register.html", role=role)
        elif not password:
            flash("Must provide a password to create an account")
            role = "alert-danger"
            return render_template("register.html", role=role)
        elif password != request.form.get("confirmation"):
            flash("Passwords don't match, please check for typos")
            role = "alert-danger"
            return render_template("register.html", role=role)
        elif not email:
            flash("Must provide an email to create an account")
            role = "alert-danger"
            return render_template("register.html", role=role)

        # Check if username exists in db
        check = db.execute("SELECT username FROM users WHERE username = (?)", username)

        if check:
            flash("The username provided is already registered")
            return render_template("register.html")
        else:
            # Include password in db
            hash = generate_password_hash(password)
            db.execute(
                "INSERT INTO users (username, hash, email) VALUES (?, ?, ?)",
                username,
                hash,
                email,
            )

            # Assign id to current session
            new_user = db.execute(
                "SELECT id FROM users WHERE username = (?) AND hash = (?)",
                username,
                hash,
            )
            session["user_id"] = new_user[0]["id"]

            # Redirect to home
            flash("Account created, welcome to Local Store!")
            role = "alert-success"
            return render_template("index.html", role=role)
    else:
        return render_template("register.html")


@app.route("/store", methods=["GET", "POST"])
@login_required
def store():
    if request.method == "POST":
        # Get all the information submitted
        store_id = request.form.get("store_id")
        products = request.form.getlist("product")
        quantities = request.form.getlist("qty")

        # Check if the order is empty
        if all(int(qty) == 0 for qty in quantities):
            flash(
                "Your order is empty. Please select products before proceeding to checkout."
            )
            role = "alert-danger"
            # Redirect back to the checkout page
            return redirect(url_for("store", store_id=store_id, role=role))

        store = db.execute("SELECT name FROM stores WHERE id = (?)", store_id)
        store = store[0]["name"]

        order_products = []
        temp_order = []
        order_total = 0

        for idx, value in enumerate(products):
            if products[idx]:
                subtotal = 0
                product_id = products[idx]
                quantity = int(quantities[idx])

                if quantity > 0:
                    product = db.execute(
                        "SELECT cents, product FROM products WHERE id = (?)", product_id
                    )

                    cents = product[0]["cents"] / 100
                    subtotal = cents * quantity
                    order_total += subtotal
                    temp_order.append(
                        {
                            "product_id": product_id,
                            "store_id": store_id,
                            "qty": quantity,
                        }
                    )
                    order_products.append(
                        {
                            "product": product[0]["product"],
                            "qty": quantity,
                            "cents": f"{cents:.2f}",
                            "subtotal": f"{subtotal:.2f}",
                        }
                    )

        order_total = f"{order_total:.2f}"
        # Saving the order info to the session
        session["temp_order"] = temp_order
        # Create a temporary table that will have all the order information
        return render_template(
            "checkout.html",
            order_products=order_products,
            order_total=order_total,
            store=store,
        )

    else:
        # Get the store id to start gathering the rest of the information from the database
        store_id = request.args.get("store_id")
        # Select store name by ID
        store_name = db.execute("SELECT name FROM stores WHERE id = (?)", store_id)
        store_name = store_name[0]["name"]
        # Select all the products to print
        products = db.execute(
            "SELECT id, product, cents FROM products WHERE store_id = (?)", store_id
        )
        # Render page with products values
        return render_template(
            "store.html",
            products=products,
            store_name=store_name,
            store_id=store_id,
            role=request.args.get("role"),
        )


@app.route("/checkout", methods=["POST"])
@login_required
def checkout():
    # Retrieve the order details from the session
    temp_order = session.get("temp_order")
    store_id = temp_order[0]["store_id"]

    if not temp_order:
        # Handle the case where order details are not available in the session
        flash("An error occured when fetching your order, please try ordering again")
        role = "alert-danger"
        return render_template("local-stores.html", role=role)

    # Insert the order record into the orders table
    db.execute(
        "INSERT INTO orders (user_id, store_id) VALUES (?, ?)",
        session["user_id"],
        store_id,
    )

    # Get the last inserted row ID using a separate SELECT statement
    order_id = db.execute("SELECT id FROM orders ORDER BY id DESC LIMIT 1")

    # Process and store the order in the database (orders and order_line tables)
    for order_product in temp_order:
        product_id = int(order_product["product_id"])
        qty = order_product["qty"]

        db.execute(
            "INSERT INTO order_line (order_id, product_id, qty) VALUES (?, ?, ?)",
            order_id[0]["id"],
            product_id,
            qty,
        )

    # Clear the order details from the session
    session.pop("temp_order", None)

    # Select the store name
    store = db.execute("SELECT name FROM stores WHERE id = (?)", store_id)

    # Redirect to a thank you page or display a success message
    return render_template(
        "success.html", store=store[0]["name"], order_id=order_id[0]["id"]
    )


@app.route("/local-stores", methods=["GET"])
@login_required
def localstores():
    stores = db.execute("SELECT id, name, img FROM stores")
    return render_template("local-stores.html", stores=stores)


@app.route("/orders", methods=["GET", "POST"])
@login_required
def myorders():
    if request.method == "POST":
        order_id = request.form.get("order_id")
        order_data = db.execute(
            "SELECT o.date, s.name FROM orders AS o JOIN stores AS s ON s.id = o.store_id WHERE o.id = (?)",
            order_id,
        )
        order_date = order_data[0]["date"]
        order_name = order_data[0]["name"]

        order_products = db.execute(
            "SELECT product_id, qty, p.product, p.cents FROM order_line JOIN products as p ON p.id = product_id WHERE order_id = (?) ORDER BY p.id ASC",
            order_id,
        )
        total = 0
        order = []

        for i in range(len(order_products)):
            subtotal = 0
            product_name = order_products[i]["product"]
            product_price = order_products[i]["cents"]
            product_qty = order_products[i]["qty"]
            # Calculate cents
            product_price = product_price / 100
            product_price = f"{product_price:.2f}"

            subtotal = float(product_price) * int(product_qty)
            total += subtotal
            subtotal = f"{subtotal:.2f}"

            order.append(
                {
                    "product": product_name,
                    "price": product_price,
                    "qty": product_qty,
                    "subtotal": subtotal,
                }
            )

        total = f"{total:.2f}"
        return render_template(
            "myorder.html",
            order=order,
            total=total,
            order_data=order_data,
            order_id=order_id,
            order_date=order_date,
            order_name=order_name,
        )
    else:
        orders = db.execute(
            "SELECT o.id, o.date, s.name FROM orders AS o JOIN stores AS s ON s.id = o.store_id WHERE user_id = (?)",
            session["user_id"],
        )
        return render_template("orders.html", orders=orders)


@app.route("/wip", methods=["GET"])
def wip():
    return render_template("wip.html")
