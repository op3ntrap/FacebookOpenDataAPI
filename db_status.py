from pymongo import MongoClient

count = 0 
client = MongoClient()
db = client.db
collec = db.instagram_buzz

collec_crsr = collec.find()
image_count = 0
for record in collec_crsr:
	
	count+=1
	for value in record['buzz']:
		image_count+=1

print "Locations_indexed :" , count
print  "Total images : " , image_count
