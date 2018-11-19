import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    portfolio = db.execute("SELECT shares, symbol FROM portfolio WHERE id = :id", id=session["user_id"])
    if not portfolio:
        return apology("didn't buy any stock", 403)
    # creat an account to store the cash + stock worthy
    fairvalue = 0
    for portfolio in portfolio:
        symbol = portfolio["symbol"]
        shares = portfolio["shares"]
        price = lookup(symbol)
        fairvalue += price["price"]*shares
        db.execute("UPDATE portfolio SET price=:price, total=:total WHERE id=:id AND symbol=:symbol", price=usd(price["price"]), total=usd(fairvalue), id=session["user_id"], symbol=symbol)
    cash = db.execute("SELECT cash FROM users WHERE id=:id", id=session["user_id"])
    fairvalue += cash[0]["cash"]
    updated_portfolio = db.execute("SELECT * FROM portfolio WHERE id=:id", id=session["user_id"])
    return render_template("index.html", portfolio=updated_portfolio, cash=usd(cash[0]["cash"]), fairvalue=usd(fairvalue))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        if not request.form.get("symbol") or not request.form.get("shares"):
            return apology("missing symbol or shares", 403)

        symbol = lookup(request.form.get("symbol"))
        if symbol is None:
            apology("invalid symbol!", 400)

        shares = int(request.form.get("shares"))
        if shares < 0:
            apology("invalid number!", 400)

        checkcash = db.execute("SELECT cash FROM users WHERE id = :id", id = session["user_id"])
        if float(checkcash[0]["cash"]) < float(symbol["price"] * shares):
            return apology("don't have enough money", 400)

        db.execute("INSERT INTO histories (symbol, shares, price, id) VALUES(:symbol, :shares, :price, :id)", symbol=symbol["symbol"],
                    shares=shares, price=usd(symbol["price"]), id=session["user_id"])
        #update users cash balance
        db.execute("UPDATE users SET cash=cash-:purchase WHERE id = :id", purchase=symbol["price"]*shares, id=session["user_id"])

        usershares = db.execute("SELECT shares FROM portfolio WHERE id = :id AND symbol = :symbol", id=session["user_id"], symbol=symbol["symbol"])
        if not usershares:
            db.execute("INSERT INTO portfolio (id, symbol, name, shares, price, total) VALUES(:id, :symbol, :name, :shares, :price, :total)",
                        id=session["user_id"], symbol=symbol["symbol"], name=symbol["name"], shares=shares, price=usd(symbol["price"]), total=usd(shares*symbol["price"]))
        else:
            updateshares = shares + usershares[0]["shares"]
            db.execute("UPDATE portfolio SET shares = :updateshares WHERE id = :id AND symbol = :symbol", updateshares=updateshares, id=session["user_id"], symbol=symbol["symbol"])
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    histories = db.execute("SELECT * FROM histories WHERE id = :id", id=session["user_id"])
    if not histories:
        return apology("didn't buy any stocks", 403)
    return render_template("history.html", histories=histories)


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

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
        if not request.form.get("symbol"):
            return apology("Missing Symbol", 400)
        quote = lookup(request.form.get("symbol"))
        if quote is None:
            return apology("invalid symbol!", 400)
        else:
            return render_template("quoted.html", stock=quote)
    else:
        return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()
    """Register user"""
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("Missing username!", 403)
        elif not request.form.get("password") or request.form.get("password") != request.form.get("passwordconfirm"):
            return apology("Missing password!", 403)
        hash = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)
        result = db.execute("INSERT INTO users(username, hash) VALUES(:username, :hash)", username=request.form.get("username"), hash=hash)
        if not result:
            return apology("username already exist!", 403)
        else:
            session["user_id"] = result
            return redirect("/")
    else:
        return render_template("register.html")
@app.route("/sell", methods=["GET", "POST"])
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        stocks = db.execute("SELECT * FROM portfolio WHERE id=:id", id=session["user_id"])
        return render_template("sell.html", stocks=stocks)
    else:
        #store the stock want to sell
        if not request.form.get("symbol") or not request.form.get("shares") or int(request.form.get("shares"))< 1:
            return apology("invalid request!", 403)
        symbol = request.form.get("symbol")
        #number want to sell
        shares = int(request.form.get("shares"))
        #check whether the user's account has enough shares of the stock
        checkcount = db.execute("SELECT shares FROM portfolio WHERE id=:id AND symbol=:symbol",
        id=session["user_id"], symbol=symbol)
        if not checkcount or shares > checkcount[0]["shares"]:
            return apology("invalid request!", 403)

        #get the updating info of the stock
        stockupdate = lookup(symbol)
        #new trading history
        db.execute("INSERT INTO histories (symbol, shares, price, id) VALUES (:symbol, :shares, :price, :id)",
        symbol=symbol, shares=-shares, price=usd(stockupdate["price"]), id=session["user_id"])

        #creat a newshares VAR for the use of updating portfolio
        newshares =  checkcount[0]["shares"]- shares
        # if newshares < 0 => DELETE this portfolio
        if newshares <= 0:
            db.execute("DELETE FROM portfolio WHERE id=:id AND symbol=:symbol",
            id=session["user_id"], symbol=symbol)
        # or update the newshares and price
        else:
            db.execute("UPDATE portfolio SET shares=:newshares, price=:price WHERE id=:id AND symbol=:symbol",
            newshares=newshares, price=usd(stockupdate["price"]), id=session["user_id"], symbol=symbol)
        # prepare for update cash account in user
        db.execute("UPDATE users SET cash=cash+:cash WHERE id=:id",
        id=session["user_id"], cash=float(shares*stockupdate["price"]))
        return redirect("/")

def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)

@app.route("/changepassword", methods=["GET", "POST"])
@login_required
def changepassword():
    if request.method == "POST":
        if not request.form.get("oldpassword"):
            return apology("missing password!", 400)
        # identify the user
        old = request.form.get("oldpassword")
        # confirm old
        confirmold = db.execute("SELECT hash FROM users WHERE id=:id", id=session["user_id"])
        if not check_password_hash(confirmold[0]["hash"], request.form.get("oldpassword")):
            return apology("wrong password!", 403)
        new = request.form.get("newpassword")
        if new != request.form.get("newpassword"):
            return apology("wrong password!", 403)
        hash = generate_password_hash(request.form.get("newpassword"), method='pbkdf2:sha256', salt_length=8)
        result = db.execute("UPDATE users SET hash=:hash WHERE id=:id", id=session["user_id"], hash=hash)
        if not result:
            return apology("failed!", 400)
        else:
            session.clear()
            return redirect("/")
    else:
        return render_template("changepassword.html")


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
