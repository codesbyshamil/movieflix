from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import os

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

app.secret_key = "movieflix_secret"

DATABASE = "/tmp/database.db" if os.environ.get("VERCEL") else "database.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


try:
    init_db()
except:
    pass


MOVIES = [
    {
        "id":1,
        "title":"Money Heist",
        "genre":"Action",
        "language":"English",
        "image":"https://image.tmdb.org/t/p/w500/reEMJA1uzscCbkpeRJeTT2bjqUp.jpg",
        "cast":"Álvaro Morte, Úrsula Corberó"
    }
]


@app.route("/",methods=["GET","POST"])
def login():

    error=None

    if request.method=="POST":

        email=request.form["email"]
        password=request.form["password"]

        try:

            conn=get_db()

            user=conn.execute(
                "SELECT * FROM users WHERE email=? AND password=?",
                (email,password)
            ).fetchone()

            conn.close()

            if user:

                session["user"]=user["username"]

                return redirect(
                    url_for("dashboard")
                )

            error="Invalid credentials"

        except Exception as e:

            error=str(e)

    return render_template(
        "login.html",
        error=error
    )


@app.route("/signup",methods=["GET","POST"])
def signup():

    error=None

    if request.method=="POST":

        username=request.form["username"]
        email=request.form["email"]
        password=request.form["password"]

        try:

            conn=get_db()

            conn.execute(
                """
                INSERT INTO users
                (username,email,password)
                VALUES(?,?,?)
                """,
                (username,email,password)
            )

            conn.commit()
            conn.close()

            session["user"]=username

            return redirect(
                url_for("dashboard")
            )

        except Exception as e:

            error=str(e)

    return render_template(
        "signup.html",
        error=error
    )


@app.route("/dashboard")
def dashboard():

    if "user" not in session:

        return redirect(
            url_for("login")
        )

    return render_template(
        "dashboard.html",
        movies=MOVIES
    )


@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )


if __name__=="__main__":
    app.run(debug=True)