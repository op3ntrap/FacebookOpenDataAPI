from pymongo import MongoClient as mg
client = mg()


def dispose(array_r,page_id):
    new_db = client.fb_feed[page_id]
    if len (array_r) > 2:
        for a in array_r:
            new_db.insert_one (a)
    if len (array_r) == 1:
        for feed in array_r[0]:
            new_db.insert_one(feed)



for a in client.db.page_feed.find():
    dispose (a['feed'], a['pageid'])
