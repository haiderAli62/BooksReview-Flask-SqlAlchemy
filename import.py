import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session , sessionmaker


engine = create_engine("postgres://bmtwqsvxbqiqed:4c270f18e4f42a0b16c0dbfa531de661fc0893523836138cfbd7e09ced5cdb50@ec2-107-21-98-165.compute-1.amazonaws.com:5432/dbml57km45qnos")
db = scoped_session(sessionmaker(bind=engine))


def main():
    """
    names = []
    ratings = db.execute(f"SELECT * FROM reviews WHERE isbn='0380795272' ").fetchall()
    ratings = [1,2]
    print(ratings)
    for r in ratings:
    	name = db.execute(f"SELECT f_name FROM users WHERE id = {r} ").fetchone()
    	print(name )
    	names.append(name)
    print(names)	 """

    values = db.execute("SELECT * FROM books where isbn = '0380795272' ").fetchone()
    title = values[1]
    author = values[2]
    year = values[3]

    print(f"title : {title} , author : {author} , year : {year} ")



    """
    f = open("books.csv")
    books = csv.reader(f)
    for isbn , title , author ,year in books:
		db.execute("INSERT INTO books(isbn , title , author ,year) VALUES(:isbn , :title ,:author ,:year)",{
			"isbn":isbn , "title":title,"author":author,"year":year
			})

     db.commit()  """
		


	


if __name__ == "__main__":
	main()
