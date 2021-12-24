import os
from flask import Flask, flash, redirect, render_template, request, session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

import _sqlite3
import sqlite3

app = Flask(__name__)

os.urandom(12).hex()

app.secret_key = 'f3cfe9ed8fae309f02079dbf'

con = sqlite3.connect('Data.db', check_same_thread=False)
curs = con.cursor()


def is_provided(field):
    if not request.form.get(field):
        return apology(f"must provide {field}", 400)


def apology(message, code=400):
    def escape(s):
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


@app.route('/')
def main():
    return render_template('Main-page.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route("/logout")
def logout():
    session.clear()

    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":

        result_checks = is_provided("E_mail") or is_provided("password")
        if result_checks is not None:
            return result_checks

        mail = request.form.get('E_mail')
        password = request.form.get('password')

        curs.execute("SELECT E_Mail FROM USERS")
        rows = curs.execute("SELECT E_Mail,Password  FROM USERS")

        if request.form.get('E_mail') in rows:
            if request.form.get('password') in rows:
                return apology("invalid e-mail and/or password", 403)

        return redirect("/home")

    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        result_checks = is_provided("fname") or is_provided("lname") or is_provided("password") or \
                        is_provided("email")

        if result_checks is not None:
            return result_checks

        if request.form.get("password") != request.form.get("confirmation"):
            return apology("Password must match")

        f_name = request.form.get("fname")
        l_name = request.form.get("lname")
        e_mail = request.form.get("email")
        password = request.form.get("password")

        curs.execute("INSERT INTO Users (F_name, L_name,  E_Mail, Password) VALUES "
                     "[:f_name, :l_name, :e_mail, :password]")

        curs.commit()
        curs.close()

        return redirect("/")

    else:
        return render_template("Registration.html")
