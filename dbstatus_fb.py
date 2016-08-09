from pymongo import MongoClient
db= MongoClient().db.page_feed
count = 0
for a in db.find():
	try:
		count+=len(a['feed'][0])
	except IndexError:
		print a['pageid']
print count
