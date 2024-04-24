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
db = SQL("sqlite:///vinbox.db")

@app.after_request
def after_request(response):

    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":
        email = request.form.get("email")

        check = db.execute("SELECT email FROM newsletter WHERE email = (?)", email)
        check_user = db.execute("SELECT email FROM users WHERE email = (?)", email)

        reserved = db.execute("SELECT reserved FROM stock WHERE product_id = 1")
        stock = db.execute("SELECT stock FROM stock WHERE product_id = 1")
        left = stock[0]["stock"] - reserved[0]["reserved"]

        if reserved[0]["reserved"] < 0:
            percentage = '0%'
        else:
            percentage = int((reserved[0]["reserved"] * 100) / stock[0]["stock"])
            percentage = str(percentage) + '%'

        db.execute("UPDATE stock SET left = (?) WHERE product_id = 1", left)
        db.execute("UPDATE stock SET percentage = (?) WHERE product_id = 1", percentage)

        stock_left = db.execute("SELECT left FROM stock WHERE product_id = 1")
        stock_left = stock_left[0]["left"]
        percentage = db.execute("SELECT percentage FROM stock WHERE product_id = 1")
        percentage = percentage[0]["percentage"]

        if check_user:
            flash(f"El email utilzado ya tiene cuenta Vinbox.")
            role = 'alert-danger'
            return render_template('index.html', role=role, stock_left=stock_left, percentage=percentage)
        elif check:
            flash(f"El email utilizado ya está suscrito a la newsletter.")
            role = 'alert-warning'
            return render_template('index.html', role=role, stock_left=stock_left, percentage=percentage)
        else:
            db.execute("INSERT INTO newsletter (email) VALUES (?)", email)
            flash(f"¡Muchas gracias! Pronto recibirás noticias sobre el próximo lote.")
            role = 'alert-success'
            return render_template('index.html', role=role, stock_left=stock_left, percentage=percentage)
    else:
        reserved = db.execute("SELECT reserved FROM stock WHERE product_id = 1")
        stock = db.execute("SELECT stock FROM stock WHERE product_id = 1")
        left = stock[0]["stock"] - reserved[0]["reserved"]

        if reserved[0]["reserved"] < 0:
            percentage = '0%'
        else:
            percentage = int((reserved[0]["reserved"] * 100) / stock[0]["stock"])
            percentage = str(percentage) + '%'

        db.execute("UPDATE stock SET left = (?) WHERE product_id = 1", left)
        db.execute("UPDATE stock SET percentage = (?) WHERE product_id = 1", percentage)

        stock_left = db.execute("SELECT left FROM stock WHERE product_id = 1")
        stock_left = stock_left[0]["left"]
        percentage = db.execute("SELECT percentage FROM stock WHERE product_id = 1")
        percentage = percentage[0]["percentage"]

        return render_template("index.html", stock_left=stock_left, percentage=percentage)

@app.route("/profile", methods=["GET"])
@login_required
def profile():

    user_data = db.execute("SELECT * FROM users WHERE id = (?)", session["user_id"])
    user_historic = db.execute("SELECT * FROM historic WHERE id = (?)", session["user_id"])
    return render_template("profile.html", user_data=user_data, user_historic=user_historic)

@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    if request.method == "POST":

        # Ensure username and password where inputed
        email = request.form.get("email")
            # AGREGAR ERRORES

        password = request.form.get("password")
            # AGREGAR ERRORES

        # Query db to know if username + password exist and are correct
        rows = db.execute("SELECT * FROM users WHERE email = (?)", email)
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            # flash("Username or password not correct")
            return render_template("login.html")

        # Remember user
        session["user_id"] = rows[0]["id"]

        # Send user to home page
        return redirect("/")
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        # Retrieve email and password from inputs
        email = request.form.get("email")
        password = request.form.get("password")

        # Check info is correct
        if not email:
            flash("ERROR")
            return render_template("/register")
        elif not password:
            flash("ERROR")
            return render_template("/register")
        elif password != request.form.get("confirm"):
            flash("ERROR")
            return render_template("/register")

        # Check if email exists in db
        check = db.execute("SELECT email FROM users WHERE email = (?)", email)

        if check:
            flash("ERROR")
            return render_template("/register")
        else:
            # Include user in db
            hash = generate_password_hash(password)
            db.execute("INSERT INTO users (email, hash) VALUES (?, ?)", email, hash)

            # Assign id to current session
            new_user = db.execute("SELECT id FROM users WHERE email = (?) AND hash = (?)", email, hash)
            session["user_id"] = new_user[0]["id"]

            # Redirect to home
            flash("Registered correctly")
            return redirect("/")
    else:
        return render_template("register.html")

@app.route("/product", methods=["GET", "POST"])
def product():

    if request.method == "POST":
        reserved = request.form.get("cantidad")
        if reserved == '1':
            one_checked = 'checked'
            return render_template("checkout.html", one_checked=one_checked)
        else:
            two_checked = 'checked'
            return render_template("checkout.html", two_checked=two_checked)
    else:
        product_id = request.args.get("product_id")
        # Check product stock in db
        reserved = db.execute("SELECT reserved FROM stock WHERE product_id = (?)", product_id)
        stock = db.execute("SELECT stock FROM stock WHERE product_id = (?)", product_id)
        left = stock[0]["stock"] - reserved[0]["reserved"]

        if reserved[0]["reserved"] < 0:
            percentage = '0%'
        else:
            percentage = int((reserved[0]["reserved"] * 100) / stock[0]["stock"])
            percentage = str(percentage) + '%'

        db.execute("UPDATE stock SET left = (?) WHERE product_id = (?)", left, product_id)
        db.execute("UPDATE stock SET percentage = (?) WHERE product_id = (?)", percentage, product_id)

        stock_left = db.execute("SELECT left FROM stock WHERE product_id = (?)", product_id)
        stock_left = stock_left[0]["left"]
        percentage = db.execute("SELECT percentage FROM stock WHERE product_id = (?)", product_id)
        percentage = percentage[0]["percentage"]
        wine = db.execute("SELECT wine, store, year, variety, origin, presentation FROM products WHERE id = (?)", product_id)


        return render_template("product.html", product_id=product_id, stock_left=stock_left, percentage=percentage, wine=wine)

@app.route("/checkout", methods=["GET", "POST"])
def checkout():

    if request.method == "POST":
        reserve = int(request.form.get("cantidad"))

        # Check db for stock
        stock = db.execute("SELECT stock, reserved FROM stock WHERE id = 1")
        check = stock[0]["reserved"] + reserve

        # Check for enough stock
        if stock[0]["stock"] == check or stock[0]["stock"] < check:
            role = 'alert-danger'
            flash(f"Lo sentimos, no hay suficiente stock para realizar la compra")
            return render_template("checkout.html", role=role)
        else:
            db.execute("UPDATE stock SET reserved = (?) WHERE product_id = 1", check)
            return render_template("success.html")

    else:
        reserved = request.args.get("cantidad")

        if reserved == '1':
            one_checked = 'checked'
            return render_template("checkout.html", one_checked=one_checked)
        else:
            two_checked = 'checked'
            return render_template("checkout.html", two_checked=two_checked)

@app.route("/bodegas", methods=["GET", "POST"])
def bodegas():

    if request.method == "POST":
        name = request.form.get("nombre")
        email = request.form.get("email")
        msg = request.form.get("msg")

        db.execute("INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)", name, email, msg)
        flash("Mensaje enviado! Te contactaremos a la brevedad")
        return render_template("bodegas.html")
    else:
        return render_template("bodegas.html")