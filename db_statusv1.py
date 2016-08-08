from pymongo import MongoClient

db = MongoClient().db.user_media	
crsr = db.find()

count = 0 
c = 0

for a in crsr:
	try:
		c+=1
		count+=len(a['user_media'])
	except KeyError:
		continue
print "doc",c
print "er", count