
import requests
#res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "1YN7MUPGPkRquipKyqpjwg", "isbns": "9781632168146"})
res = requests.get("http://127.0.0.1:5000/api/0380795272/")
revs = res.json()
print(revs)

"""
revs = revs["books"]
avg_rating = revs[0]["average_rating"]
num_of_rating = revs[0]["work_ratings_count"]
"""
#title = revs[0]["title"]
#author = revs[0]["author"]
#year = revs[0]["year"]
"""
isbn = revs[0]["isbn"]
review_count = revs[0]['reviews_count']
average_score = revs[0]["average_rating"]

print(isbn)
print(review_count)
print(average_score)

"""
#print(revs['work_ratings_count'],revs['average_rating'])




"""
rating =  [(1, 5, 'VERY GOOD', '0380795272') ,(2, 7, 'VERY GOOD', '0380795272'),(3, 8, 'VERY GOOD', '0380795272') ]
for r in rating:
	print(r[:][0])

	"""