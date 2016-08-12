from pymongo import MongoClient as mg
from pymongo import MongoClient as e
host = '104.197.108.172'
client = mg(host)
user_name= raw_input("username : ")
password = raw_input("password :")
client.db.authenticate(user_name,password,mechanism='SCRAM-SHA-1')
new_client = e()

for a in new_client.db['page_feed'].find():
    client.db.page_feed.insert_one(a)