from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import os

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

app.secret_key = "movieflix_secret"

DATABASE = "database.db"


# Database Connection
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# Create Table
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


init_db()


# Movie Data
MOVIES = [

    {"id":1,"title":"Money Heist","genre":"Action","language":"English","image":"https://image.tmdb.org/t/p/w500/reEMJA1uzscCbkpeRJeTT2bjqUp.jpg","cast":"Álvaro Morte, Úrsula Corberó, Itziar Ituño"},

    {"id":2,"title":"Interstellar","genre":"Sci-Fi","language":"English","image":"https://image.tmdb.org/t/p/w500/rAiYTfKGqDCRIIqo664sY9XZIvQ.jpg","cast":"Matthew McConaughey, Anne Hathaway, Jessica Chastain"},

    {"id":3,"title":"Avengers Endgame","genre":"Action","language":"English","image":"https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9sl16pB3iy.jpg","cast":"Robert Downey Jr, Chris Evans, Scarlett Johansson"},

    {"id":4,"title":"Batman","genre":"Action","language":"English","image":"https://image.tmdb.org/t/p/w500/74xTEgt7R36Fpooo50r9T25onhq.jpg","cast":"Robert Pattinson, Zoë Kravitz, Jeffrey Wright"},

    {"id":5,"title":"Joker","genre":"Drama","language":"English","image":"https://image.tmdb.org/t/p/w500/udDclJoHjfjb8Ekgsd4FDteOkCU.jpg","cast":"Joaquin Phoenix, Robert De Niro, Zazie Beetz"},

    {"id":6,"title":"Naruto","genre":"Anime","language":"Japanese","image":"https://image.tmdb.org/t/p/w500/xppeysfvDKVx775MFuH8Z9BlpMk.jpg","cast":"Junko Takeuchi, Chie Nakamura, Noriaki Sugiyama"},

    {"id":7,"title":"One Piece","genre":"Anime","language":"Japanese","image":"https://image.tmdb.org/t/p/w500/2rmK7mnchw9Xr3XdiTFSxTTLXqv.jpg","cast":"Mayumi Tanaka, Kazuya Nakai, Akemi Okamura"},

    {"id":8,"title":"Frozen","genre":"Kids","language":"English","image":"https://image.tmdb.org/t/p/w500/kgwjIb2JDHRhNk13lmSxiClFjVk.jpg","cast":"Idina Menzel, Kristen Bell, Jonathan Groff"},

    {"id":9,"title":"Toy Story","genre":"Kids","language":"English","image":"https://image.tmdb.org/t/p/w500/uXDfjJbdP4ijW5hWSBrPrlKpxab.jpg","cast":"Tom Hanks, Tim Allen, Joan Cusack"},

    {"id":10,"title":"Kung Fu Panda","genre":"Kids","language":"English","image":"https://image.tmdb.org/t/p/w500/wWt4JYXTg5Wr3xBW2phBrMKgp3x.jpg","cast":"Jack Black, Angelina Jolie, Dustin Hoffman"},

    {"id":11,"title":"Leo","genre":"Action","language":"Tamil","image":"https://image.tmdb.org/t/p/w500/kYgQzzjNis5jJalYtIHgrom0gOx.jpg","cast":"Vijay, Trisha Krishnan, Sanjay Dutt"},

    {"id":12,"title":"Vikram","genre":"Action","language":"Tamil","image":"https://www.themoviedb.org/t/p/w1280/774UV1aCURb4s4JfEFg3IEMu5Zj.jpg","cast":"Kamal Haasan, Vijay Sethupathi, Fahadh Faasil"},

    {"id":13,"title":"Lucifer","genre":"Action","language":"Malayalam","image":"https://www.themoviedb.org/t/p/w1280/fXgY2RCzoIJPhPDoyKRjaaqjIZs.jpg","cast":"Mohanlal, Vivek Oberoi, Manju Warrier"},

    {"id":14,"title":"365 Days","genre":"Drama","language":"English","image":"https://image.tmdb.org/t/p/w500/6KwrHucIE3CvNT7kTm2MAlZ4fYF.jpg","cast":"Tovino Thomas, Guru Somasundaram, Femina George"}

]


# Login Page
@app.route("/", methods=["GET","POST"])
def login():

    error=None

    if request.method=="POST":

        email=request.form["email"].strip()
        password=request.form["password"].strip()

        conn=get_db()

        user=conn.execute(
            """
            SELECT * FROM users
            WHERE email=? AND password=?
            """,
            (email,password)
        ).fetchone()

        conn.close()

        if user:

            session["user"]=user["username"]
            session["email"]=user["email"]

            return redirect(url_for("dashboard"))

        else:

            error="Invalid Email or Password"

    return render_template(
        "login.html",
        error=error
    )


# Signup Page
@app.route("/signup",methods=["GET","POST"])
def signup():

    error=None

    if request.method=="POST":

        username=request.form["username"].strip()
        email=request.form["email"].strip()
        password=request.form["password"].strip()

        if not username or not email or not password:

            error="All fields required"

        else:

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
                session["email"]=email

                return redirect(
                    url_for("dashboard")
                )

            except sqlite3.IntegrityError:

                error="Email already exists"

    return render_template(
        "signup.html",
        error=error
    )


# Dashboard
@app.route("/dashboard")
def dashboard():

    if "user" not in session:

        return redirect(
            url_for("login")
        )

    categories=sorted(
        set(
            movie["genre"]
            for movie in MOVIES
        )
    )

    return render_template(
        "dashboard.html",
        movies=MOVIES,
        categories=categories,
        user=session["user"]
    )


# Movie Details
@app.route("/movie/<int:movie_id>")
def movie(movie_id):

    if "user" not in session:

        return redirect(
            url_for("login")
        )

    movie=next(
        (
            x for x in MOVIES
            if x["id"]==movie_id
        ),
        None
    )

    if not movie:

        return redirect(
            url_for("dashboard")
        )

    return render_template(
        "movie.html",
        movie=movie
    )


# Payment
@app.route("/payment")
def payment():

    if "user" not in session:

        return redirect(
            url_for("login")
        )

    return render_template(
        "payment.html"
    )


# Logout
@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )


if __name__=="__main__":
    app.run(
        debug=True
    )