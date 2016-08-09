from pymongo import MongoClient
db= MongoClient().db.page_feed
count = 0
for a in db.find():
	count+=len(a['feed'][0])
print count
