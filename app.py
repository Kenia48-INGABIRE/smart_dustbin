from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "smartbin"


# DATABASE
def init_db():

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        email TEXT,
        password TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS dustbins(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        district TEXT,
        sector TEXT,
        cell TEXT,
        serial TEXT,
        status TEXT,
        message TEXT,
        time TEXT
    )
    """)

    conn.commit()
    conn.close()


# HOME
@app.route("/")
def home():
    return render_template("index.html")


# SIGNUP
@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        cur.execute("""
        INSERT INTO users(name, phone, email, password)
        VALUES (?, ?, ?, ?)
        """, (
            request.form["name"],
            request.form["phone"],
            request.form["email"],
            request.form["password"]
        ))

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("signup.html")


# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        cur.execute("""
        SELECT * FROM users
        WHERE email=? AND password=?
        """, (
            request.form["email"],
            request.form["password"]
        ))

        user = cur.fetchone()

        conn.close()

        if user:
            session["user"] = user[1]
            return redirect("/dashboard")

    return render_template("login.html")


# DASHBOARD
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():

    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    if request.method == "POST":

        status = request.form["status"]

        if status == "Full":
            message = "⚠️ Dustbin FULL"
        else:
            message = "✅ Dustbin OK"

        cur.execute("""
        INSERT INTO dustbins(
            district,
            sector,
            cell,
            serial,
            status,
            message,
            time
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            request.form["district"],
            request.form["sector"],
            request.form["cell"],
            request.form["serial"],
            status,
            message,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()

    cur.execute("""
    SELECT * FROM dustbins
    ORDER BY id DESC
    """)

    bins = cur.fetchall()

    conn.close()

    return render_template("dashboard.html", bins=bins)


# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)