from pymongo import MongoClient
import requests
import json
import sys
import os
import time

user_id = []

def get_user_recent_media(id):
	user_id.append(id)
	dump = requests.get("https://api.instagram.com/v1/user/media/recent"+id+"?access_token=3407738697.e029fea.8659525c7ca248f3b3fd6eb1130771e1")
	images_list = []

	i=2
    try:
        images = requests.get("https://api.instagram.com/v1/user/media/recent"+id+"?access_token=3407738697.e029fea.8659525c7ca248f3b3fd6eb1130771e1")
        data = images.json()
        for values in data['data']:
            images_list.append(values)
    except KeyError:
        return images_list
    #############################################################
    while(i<5):
       
        try:
            images = requests.get(data['pagination']['next_url'])
            
            time.sleep(7)
        
            data = images.json()
            #print data['pagination']['next_url']
        except KeyError:
            return images_list
       
        if (len(data['data']) == 0):
            break
        
        for values in data['data']:
            images_list.append(values)
        #print len(images_list)
    ##############################################################
    entry = {
	"_id" : id,
	"recent_media" : images_list
	}



    return entry
    


def user_existence(id):

	#check = user_media_db.find_one({"_id" : id })

	if (id in user_id):
		return True
	else:
		return False

def get_location_buzz(location_id):
	location_buzz = ibuzz.find_one({'id' : location_id})
	return location_buzz['buzz']


##executing script
client = MongoClient()
db = client.db
ibuzz = db['instagram_buzz']

location = []

for value in ibuzz:
	locations.append(value['id'])

user_media_db = db['user_media']
for location in locations:
	media_in_location = get_location_buzz(location)
	for media in media_in_location:
		if (user_existence(media['user']['id'])):
			continue
		try:
			user_media = get_user_recent_media(media['user']['id'])
		except KeyError: 
			continue
		entry = {
		"_id" : media['user']['id'],
		"user_media" : user_media
		}

		user_media_db.insert_one(entry)










	