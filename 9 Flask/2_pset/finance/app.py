# IMPORTANT: Tried everything but couldn't manage to make check pass the buy function. On my computer works perfectly and as intended, can't figure out what is causing the issue.

import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_portfolio = db.execute("SELECT stock_name, stock_symbol, quantity, price FROM portfolio WHERE user_id = (?) GROUP BY stock_name", session["user_id"])

    # Initialize total cash variable
    total_cash = 0
    # Loop through the user stocks and update prices
    for user_stock in user_portfolio:
        symbol = user_stock["stock_symbol"]
        shares = user_stock["quantity"]
        stock = lookup(symbol)
        share_price = stock["price"]
        share_price = usd(share_price)
        total = shares * stock["price"]
        total_cash += total
        total = usd(total)
        db.execute("UPDATE portfolio SET price = (?), total = (?) WHERE user_id = (?) AND stock_name = (?)", share_price, total, session["user_id"], symbol)
    # Print user total cash
    user_cash = db.execute("SELECT cash FROM users WHERE id = (?)", session["user_id"])
    user_cash = user_cash[0]["cash"]
    total_cash += user_cash
    user_cash = usd(user_cash)
    total_cash = usd(total_cash)
    updated_portfolio = db.execute("SELECT * FROM portfolio WHERE user_id = (?)", session["user_id"])
    return render_template("index.html", total_cash=total_cash, user_cash=user_cash, updated_portfolio=updated_portfolio)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = lookup(request.form.get("symbol"))
        if not symbol:
            return apology("Symbol does not exist. Check if it's spelled correctly")

        shares = request.form.get("shares")
        if not shares.isdigit():
            return apology("Cannot sell fractions of shares.")

        share_name = symbol["name"]
        sharePrice = usd(symbol["price"])
        totalPrice = int(shares) * sharePrice

        user_wallet = db.execute("SELECT cash FROM users WHERE id = (?)", session["user_id"])
        user_cash = usd(user_wallet[0]["cash"])
        # check if enough money
        if not user_wallet or user_cash < totalPrice:
            return apology("Not enough money in your account")
        else:
            db.execute("UPDATE users SET cash = cash - (?) WHERE id = (?)", totalPrice, session["user_id"])
            # check if has stock already
            stockInPort = db.execute("SELECT stock_name FROM portfolio WHERE user_id = (?) AND stock_name = (?)", session["user_id"], symbol["name"])
            if stockInPort:
                # actual quantity
                currentQty = db.execute("SELECT quantity FROM portfolio WHERE user_id = (?)", session["user_id"])
                finalQty = int(shares) + currentQty[0]["quantity"]
                # update stock share amount
                db.execute("UPDATE portfolio SET quantity = (?), price = (?) WHERE user_id = (?) AND stock_name = (?)", finalQty, symbol["price"], session["user_id"], symbol["name"])
            else:
                # add new stock to portfolio
                db.execute("INSERT INTO portfolio (user_id, stock_name, stock_symbol, quantity, price) VALUES (?, ?, ?, ?, ?)", session["user_id"], symbol["name"], symbol["symbol"], shares, symbol["price"])
            # update historic table
            db.execute("INSERT INTO historic (user_id, stock_name, price, quantity, transaction_type) VALUES (?, ?, ?, ?, 'Buy')", session["user_id"], symbol["name"], symbol["price"], shares)
            if int(shares) > 1:
                flash(f"{shares} {share_name}, ({sharePrice} each) shares bought correctly.")
            else:
                flash(f"{shares} {share_name} ({sharePrice} each) share bought correctly.")
            return redirect("/")
    else:
        return render_template("buy.html")

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    historic_table = db.execute("SELECT stock_name, price, transaction_type, quantity, date FROM historic WHERE user_id = (?)", session["user_id"])
    return render_template("historic.html", historic_table=historic_table)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        stock = lookup(request.form.get("symbol"))
        if stock is not None:
            return render_template("quoted.html", stock=stock)
        else:
            return apology("Symbol not found. Try another")
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        user = request.form.get("username")
        pwrd = request.form.get("password")

        # Check that form is completed correctly
        if not user:
            return apology("Must provide username")
        elif not pwrd:
            return apology("Must provide password")
        elif pwrd != request.form.get("confirmation"):
            return apology("Passwords does not match")

        checkdb = db.execute("SELECT username FROM users WHERE username = ?", user)
        if checkdb:
            return apology("Username already registered. Try another")
        else:
            # Hash password and save in db
            hash = generate_password_hash(pwrd)
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", user, hash)

            # Assign session to new user
            newuser = db.execute("SELECT id FROM users WHERE username = (?) AND hash = (?)", user, hash)
            session["user_id"] = newuser[0]["id"]
            flash("Account registered correctly!")
            return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_shares = db.execute("SELECT stock_symbol FROM portfolio WHERE user_id = (?)", session["user_id"])
    if request.method == "POST":
        # Creating variables with all user input + user portfolio
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))
        user_share_amount = db.execute("SELECT quantity FROM portfolio WHERE user_id = (?) AND stock_symbol = (?)", session["user_id"], symbol)
        # Checking for possible errors.
        if not symbol:
            return apology("Missing symbol.")
        elif not shares:
            return apology("Missing amount of shares to sell.")
        elif shares > user_share_amount[0]["quantity"]:
            return apology("Not enough shares.")
        # First success case, selling all the shares of some symbol
        elif shares == int(user_share_amount[0]["quantity"]):
            share_data = lookup(symbol)
            share_price = float(share_data["price"]) * user_share_amount[0]["quantity"]
            db.execute("DELETE FROM portfolio WHERE user_id = (?) AND stock_symbol = (?)", session["user_id"], symbol)
            db.execute("UPDATE users SET cash = cash + (?) WHERE id = (?)", share_price, session["user_id"])
            # Add transaction to historic table
            db.execute("INSERT INTO historic (user_id, stock_name, price, quantity, transaction_type) VALUES (?, ?, ?, ?, 'Sell')", session["user_id"], share_data["name"], share_data["price"], user_share_amount[0]["quantity"])
            return redirect("/")
        else:
            share_data = lookup(symbol)
            share_price = float(share_data["price"]) * int(shares)
            db.execute("UPDATE portfolio SET quantity = quantity - (?) WHERE user_id = (?) AND stock_symbol = (?)", shares, session["user_id"], share_data["symbol"])
            db.execute("UPDATE users SET cash = cash + (?) WHERE id = (?)", share_price, session["user_id"])
            db.execute("INSERT INTO historic (user_id, stock_name, price, quantity, transaction_type) VALUES (?, ?, ?, ?, 'Sell')", session["user_id"], share_data["name"], share_data["price"], shares)
            flash("Transaction completed")
            return redirect("/")
    else:
        return render_template("sell.html", user_shares=user_shares)

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    # Add money to user wallet
    if request.method == "POST":
        amount = request.form.get("add")
        if not amount:
            return apology("Must input an amount to add.")
        elif not amount.isdigit():
            return apology("Input must be a positive number.")

        else:
            db.execute("UPDATE users SET cash = cash + (?) WHERE id = (?)", amount, session["user_id"])
            flash(f"Money added to account")
            return redirect("/")
    else:
        return render_template("add.html")
