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

{"id":1,"title":"Money Heist","genre":"Action","language":"English","image":"https://image.tmdb.org/t/p/w500/reEMJA1uzscCbkpeRJeTT2bjqUp.jpg","cast":"Álvaro Morte, Úrsula Corberó"},
{"id":2,"title":"Interstellar","genre":"Sci-Fi","language":"English","image":"https://image.tmdb.org/t/p/w500/rAiYTfKGqDCRIIqo664sY9XZIvQ.jpg","cast":"Matthew McConaughey, Anne Hathaway"},
{"id":3,"title":"Avengers Endgame","genre":"Action","language":"English","image":"https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9sl16pB3iy.jpg","cast":"Robert Downey Jr, Chris Evans"},
{"id":4,"title":"Batman","genre":"Action","language":"English","image":"https://image.tmdb.org/t/p/w500/74xTEgt7R36Fpooo50r9T25onhq.jpg","cast":"Robert Pattinson, Zoë Kravitz"},
{"id":5,"title":"Joker","genre":"Drama","language":"English","image":"https://image.tmdb.org/t/p/w500/udDclJoHjfjb8Ekgsd4FDteOkCU.jpg","cast":"Joaquin Phoenix, Robert De Niro"},
{"id":6,"title":"Naruto","genre":"Anime","language":"Japanese","image":"https://image.tmdb.org/t/p/w500/xppeysfvDKVx775MFuH8Z9BlpMk.jpg","cast":"Junko Takeuchi"},
{"id":7,"title":"One Piece","genre":"Anime","language":"Japanese","image":"https://image.tmdb.org/t/p/w500/2rmK7mnchw9Xr3XdiTFSxTTLXqv.jpg","cast":"Mayumi Tanaka"},
{"id":8,"title":"Frozen","genre":"Kids","language":"English","image":"https://image.tmdb.org/t/p/w500/kgwjIb2JDHRhNk13lmSxiClFjVk.jpg","cast":"Idina Menzel"},
{"id":9,"title":"Toy Story","genre":"Kids","language":"English","image":"https://image.tmdb.org/t/p/w500/uXDfjJbdP4ijW5hWSBrPrlKpxab.jpg","cast":"Tom Hanks"},
{"id":10,"title":"Kung Fu Panda","genre":"Kids","language":"English","image":"https://image.tmdb.org/t/p/w500/wWt4JYXTg5Wr3xBW2phBrMKgp3x.jpg","cast":"Jack Black"},

{"id":11,"title":"Leo","genre":"Action","language":"Tamil","image":"https://image.tmdb.org/t/p/w500/kYgQzzjNis5jJalYtIHgrom0gOx.jpg","cast":"Vijay, Trisha"},
{"id":12,"title":"Vikram","genre":"Action","language":"Tamil","image":"https://image.tmdb.org/t/p/w500/774UV1aCURb4s4JfEFg3IEMu5Zj.jpg","cast":"Kamal Haasan"},
{"id":13,"title":"Lucifer","genre":"Action","language":"Malayalam","image":"https://image.tmdb.org/t/p/w500/fXgY2RCzoIJPhPDoyKRjaaqjIZs.jpg","cast":"Mohanlal"},
{"id":14,"title":"2018","genre":"Drama","language":"Malayalam","image":"https://image.tmdb.org/t/p/w500/tR4YlK7nP5jQx8m.jpg","cast":"Tovino Thomas"},
{"id":15,"title":"Minnal Murali","genre":"Action","language":"Malayalam","image":"https://image.tmdb.org/t/p/w500/xAG7vMq4K5M.jpg","cast":"Tovino Thomas"},

{"id":16,"title":"John Wick","genre":"Action","language":"English","image":"https://image.tmdb.org/t/p/w500/fZPSd91yGE9fCcCe6OoQr6E3Bev.jpg","cast":"Keanu Reeves"},
{"id":17,"title":"The Dark Knight","genre":"Action","language":"English","image":"https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg","cast":"Christian Bale"},
{"id":18,"title":"Inception","genre":"Sci-Fi","language":"English","image":"https://image.tmdb.org/t/p/w500/oYuLEt3zVCKq57qu2F8dT7NIa6f.jpg","cast":"Leonardo DiCaprio"},
{"id":19,"title":"The Matrix","genre":"Sci-Fi","language":"English","image":"https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg","cast":"Keanu Reeves"},
{"id":20,"title":"Titanic","genre":"Drama","language":"English","image":"https://image.tmdb.org/t/p/w500/9xjZS2rlVxm8SFx8kPC3aIGCOYQ.jpg","cast":"Leonardo DiCaprio"},

{"id":21,"title":"Breaking Bad","genre":"Thriller","language":"English","image":"https://image.tmdb.org/t/p/w500/ggFHVNu6YYI5L9pCfOacjizRGt.jpg","cast":"Bryan Cranston"},
{"id":22,"title":"Peaky Blinders","genre":"Thriller","language":"English","image":"https://image.tmdb.org/t/p/w500/vUUqzWa2LnHIVqkaKVlVGkVcZIW.jpg","cast":"Cillian Murphy"},
{"id":23,"title":"Stranger Things","genre":"Sci-Fi","language":"English","image":"https://image.tmdb.org/t/p/w500/49WJfeN0moxb9IPfGn8AIqMGskD.jpg","cast":"Millie Bobby Brown"},
{"id":24,"title":"Squid Game","genre":"Thriller","language":"Korean","image":"https://image.tmdb.org/t/p/w500/dDlEmu3EZ0Pgg93K2SVNLCjCSvE.jpg","cast":"Lee Jung-jae"},
{"id":25,"title":"The Witcher","genre":"Fantasy","language":"English","image":"https://image.tmdb.org/t/p/w500/cZ0d3rtvXPVvuiX22sP79K3Hmjz.jpg","cast":"Henry Cavill"},

{"id":26,"title":"Drishyam","genre":"Thriller","language":"Malayalam","image":"https://image.tmdb.org/t/p/w500/5f3Jw0.jpg","cast":"Mohanlal"},
{"id":27,"title":"Premam","genre":"Drama","language":"Malayalam","image":"https://image.tmdb.org/t/p/w500/abc123.jpg","cast":"Nivin Pauly"},
{"id":28,"title":"Hridayam","genre":"Drama","language":"Malayalam","image":"https://image.tmdb.org/t/p/w500/hri123.jpg","cast":"Pranav Mohanlal"},
{"id":29,"title":"Charlie","genre":"Drama","language":"Malayalam","image":"https://image.tmdb.org/t/p/w500/charlie.jpg","cast":"Dulquer Salmaan"},
{"id":30,"title":"Bangalore Days","genre":"Drama","language":"Malayalam","image":"https://image.tmdb.org/t/p/w500/bangalore.jpg","cast":"Dulquer Salmaan"},

{"id":31,"title":"Master","genre":"Action","language":"Tamil","image":"https://image.tmdb.org/t/p/w500/master.jpg","cast":"Vijay"},
{"id":32,"title":"Jailer","genre":"Action","language":"Tamil","image":"https://image.tmdb.org/t/p/w500/jailer.jpg","cast":"Rajinikanth"},
{"id":33,"title":"Beast","genre":"Action","language":"Tamil","image":"https://image.tmdb.org/t/p/w500/beast.jpg","cast":"Vijay"},
{"id":34,"title":"Kaithi","genre":"Action","language":"Tamil","image":"https://image.tmdb.org/t/p/w500/kaithi.jpg","cast":"Karthi"},
{"id":35,"title":"Thunivu","genre":"Action","language":"Tamil","image":"https://image.tmdb.org/t/p/w500/thunivu.jpg","cast":"Ajith Kumar"},

{"id":36,"title":"Demon Slayer","genre":"Anime","language":"Japanese","image":"https://image.tmdb.org/t/p/w500/demon.jpg","cast":"Natsuki Hanae"},
{"id":37,"title":"Death Note","genre":"Anime","language":"Japanese","image":"https://image.tmdb.org/t/p/w500/deathnote.jpg","cast":"Mamoru Miyano"},
{"id":38,"title":"Attack on Titan","genre":"Anime","language":"Japanese","image":"https://image.tmdb.org/t/p/w500/aot.jpg","cast":"Yuki Kaji"},
{"id":39,"title":"Dragon Ball Z","genre":"Anime","language":"Japanese","image":"https://image.tmdb.org/t/p/w500/dbz.jpg","cast":"Masako Nozawa"},
{"id":40,"title":"Jujutsu Kaisen","genre":"Anime","language":"Japanese","image":"https://image.tmdb.org/t/p/w500/jjk.jpg","cast":"Junya Enoki"},

{"id":41,"title":"Cars","genre":"Kids","language":"English","image":"https://image.tmdb.org/t/p/w500/cars.jpg","cast":"Owen Wilson"},
{"id":42,"title":"Finding Nemo","genre":"Kids","language":"English","image":"https://image.tmdb.org/t/p/w500/nemo.jpg","cast":"Albert Brooks"},
{"id":43,"title":"Moana","genre":"Kids","language":"English","image":"https://image.tmdb.org/t/p/w500/moana.jpg","cast":"Auliʻi Cravalho"},
{"id":44,"title":"Coco","genre":"Kids","language":"English","image":"https://image.tmdb.org/t/p/w500/coco.jpg","cast":"Anthony Gonzalez"},
{"id":45,"title":"Shrek","genre":"Kids","language":"English","image":"https://image.tmdb.org/t/p/w500/shrek.jpg","cast":"Mike Myers"},

{"id":46,"title":"Gladiator","genre":"Action","language":"English","image":"https://image.tmdb.org/t/p/w500/gladiator.jpg","cast":"Russell Crowe"},
{"id":47,"title":"Fast X","genre":"Action","language":"English","image":"https://image.tmdb.org/t/p/w500/fiVW06jE7z9YnO4trhaMEdclSiC.jpg","cast":"Vin Diesel"},
{"id":48,"title":"Mission Impossible","genre":"Action","language":"English","image":"https://image.tmdb.org/t/p/w500/l5uxY5m5OInWpcExIpKG6AR3rgL.jpg","cast":"Tom Cruise"},
{"id":49,"title":"Deadpool","genre":"Action","language":"English","image":"https://image.tmdb.org/t/p/w500/fSRb7vyIP8rQpL0I47P3qUsEKX3.jpg","cast":"Ryan Reynolds"},
{"id":50,"title":"Spider-Man No Way Home","genre":"Action","language":"English","image":"https://image.tmdb.org/t/p/w500/1g0dhYtq4irTY1GPXvft6k4YLjm.jpg","cast":"Tom Holland"}

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