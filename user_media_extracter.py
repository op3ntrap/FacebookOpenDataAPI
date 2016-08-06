from pymongo import MongoClient
import requests
import json
import sys
import os
import time
from simplejson.scanner import JSONDecodeError

user_id = []


def get_user_recent_media(id):
    
    #dump = requests.get(
    #   "https://api.instagram.com/v1/user/media/recent" + id + "?access_token=3407738697.e029fea.8659525c7ca248f3b3fd6eb1130771e1")
    images_list = []

    i = 2
    try:
        try:
            images = requests.get(
                "https://api.instagram.com/v1/users/"+id+"/media/recent?access_token=3407738697.e029fea.8659525c7ca248f3b3fd6eb1130771e1")
            ##print  "https://api.instagram.com/v1/users/"+id+"/media/recent?access_token=3407738697.e029fea.8659525c7ca248f3b3fd6eb1130771e1"
            url =  "https://api.instagram.com/v1/users/"+id+"/media/recent?access_token=3407738697.e029fea.8659525c7ca248f3b3fd6eb1130771e1"

            data = images.json()
        except JSONDecodeError:
            #print "json error"
            return images_list
        for values in data['data']:
            images_list.append(values)
    except KeyError:
        #print "empty data"
        return images_list
    #############################################################
    while (i < 5):
    	try:
    		max_id = data['pagination']['next_max_id']
    	except KeyError as e :
    		print "max_id"
    		break

        try:
            images2 = requests.get(url+ "&max_id=" +max_id)
            #print url+ "&max_id=" + data['pagination']['next_max_id']
            ##print images2.content
            #print "paginated 1 "

            time.sleep(7)
            #print "sleeping"

            data = images2.json()
        # #print data['pagination']['next_url']
        except KeyError:
            #print "pagination empty data returned"
            break

       
        for values in data['data']:
            images_list.append(values)
        # #print len(images_list)
    ##############################################################
    #print "finished with ", len(images_list)
    return images_list


def user_existence(id):
    # type: (result) -> bool
    if (id in user_id):
        return True
    else:
        return False


def get_location_buzz(location_id):
    location_buzz = ibuzz.find_one({'id': location_id})
    return location_buzz['buzz']


##executing script
client = MongoClient()
db = client.db
ibuzz = db['instagram_buzz']

locationids = []

for value in ibuzz.find():
    locationids.append(value['id'])

user_media_db = db['user_media']
for users in user_media_db.find():
	user_id.append(users['id'])

for location in locationids:
    media_in_location = get_location_buzz(location)
    for media in media_in_location:
        
        
        user_media = get_user_recent_media(media['user']['id'])
   
        entry = {
            "id": media['user']['id'],
            "user_media": user_media
        }

        user_media_db.insert_one(entry)
        user_id.append(id)
