import requests
from flask import jsonify
from flask import Flask, session , render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not "postgres://bmtwqsvxbqiqed:4c270f18e4f42a0b16c0dbfa531de661fc0893523836138cfbd7e09ced5cdb50@ec2-107-21-98-165.compute-1.amazonaws.com:5432/dbml57km45qnos":
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine("postgres://bmtwqsvxbqiqed:4c270f18e4f42a0b16c0dbfa531de661fc0893523836138cfbd7e09ced5cdb50@ec2-107-21-98-165.compute-1.amazonaws.com:5432/dbml57km45qnos")
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/success" , methods=["POST"])
def success():
    first_name = request.form.get("fname")
    last_name = request.form.get("lname")
    username  = request.form.get("username")
    password = request.form.get("password")

    db.execute(f"INSERT INTO users(f_name , l_name , username ,password) values (:first_name , :last_name, :username , :password) ",
		{"first_name" : first_name ,"last_name":last_name ,"username":username, "password":password ,})
    db.commit()
    return render_template("login.html")

@app.route("/home" , methods=["POST","GET" ])
def home():
    user = request.form.get("username")
    passwrd = request.form.get("password")

    if db.execute(f"SELECT * FROM users where username = :username and password=:password ",
		{"username":user , "password":passwrd}).rowcount == 0 :
        return render_template("login.html" , message="Invalid username or password")

    books =  db.execute("SELECT * FROM books").fetchall()
    return render_template("home.html" , books=books)

@app.route("/search" , methods=["GET"])
def search():
    keyword = request.args.get("search")
    items = db.execute(f""" SELECT * FROM books WHERE isbn = '{keyword}' OR 
		    title = '{keyword}' OR author = '{keyword}'   OR isbn LIKE '%{keyword}%' OR 
		    title LIKE '%{keyword}%' OR author LIKE '%{keyword}%' """).fetchall()
    
    return render_template("search.html" , items=items)

@app.route("/book/<isb>" , methods=["GET"])
def book(isb):
    isb = str(isb)


    book = db.execute(f"SELECT * FROM books WHERE isbn ='{isb}' ").fetchone()
    print(book)
    ratings = db.execute(f"SELECT * FROM reviews WHERE isbn='{isb}' ").fetchall()
    names = []
    for r in ratings:
    	name = db.execute(f"SELECT f_name FROM users WHERE id = {r[:][0]} ").fetchone()
    	print(name )
    	names.append(name)

    print(f"Ratings : {ratings} Name : {names} ")
    zip_data = zip(ratings,names)

    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "1YN7MUPGPkRquipKyqpjwg", "isbns": "9781632168146"})
    revs = res.json()
    revs = revs["books"]
    avg_rating = revs[0]["average_rating"]
    num_of_rating = revs[0]["work_ratings_count"]



    return render_template("book.html" , book=book , zip_data=zip_data, avg_rating=avg_rating , num_of_rating=num_of_rating)

@app.route("/rating/<isb>" , methods=["GET"])
def rating(isb):
    isb = str(isb)

    star = request.args.get("star")
    comment = request.args.get("text")
    db.execute(f"INSERT INTO reviews(rating , comment , isbn) values({star} , '{comment}' , '{isb}' ) ")
    print(f"inserted {isb}  , {star} stars  , {comment} ")
    db.commit()
    return render_template("book.html")
    
@app.route("/api/<isbn>" , methods=["GET"])
def api(isbn):
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "1YN7MUPGPkRquipKyqpjwg", "isbns": "9781632168146"})
    revs = res.json()
    revs = revs["books"]

    values = db.execute("SELECT * FROM books where isbn = '0380795272' ").fetchone()
    title = values[1]
    author = values[2]
    year = values[3]

    isbn = revs[0]["isbn"]
    review_count = revs[0]['reviews_count']
    average_score = revs[0]["average_rating"]
    return jsonify({
            "title" :  title,
            "author" :  author, 
            "year" : year, 
            "isbn" : isbn,
            "review_count": review_count   ,
            "average_score" : average_score
            })


