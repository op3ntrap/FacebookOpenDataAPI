from pymongo import MongoClient
import requests
import time

#database initialization
access_token = "EAACNrjHuFp0BALzPRibHAQANNMt0pTZAkZAWtmZAgBUFBtIvx2RzYUwXZCtbdp6c0z9nNGMAZCBAp302ilvRU3ybtkMsAVwDeGmQDiTOZAJbJggbWo46A96tpoAPeBfUDZA2nlGAc88qsAthGCPSOaNJVWJNkYZAocMZD"


def paginator(next_url):
	#print "executed"
	data = []
	while(True):
		try:
			dump = requests.get(next_url)
			feed = dump.json()
			data = feed['data'] + data
		except KeyError:
			break
	return data


#feed datarequest
def feed_request(pageid,until,since):
	#print "executed"
	try:
		data_request = requests.get(
			"https://graph.facebook.com/v2.7/" + str(pageid) + "/feed?limit=100&since=" + str(since) + "&until=" + str(until) + "&access_token=" + access_token)
		data = data_request.json()
		print data
	except KeyError:
		return None
	print "here2"
	final_data = paginator (data['paging']['next'])
	final_data = final_data + data['data']
	return final_data





def get_page_daily_feed(pageid):
	page_feed = []
	current_time = time.time()
	time_constant = 86400
	current_time = int(time.time())
	while (current_time>0):
		try:
			print "here"
			initial_data = feed_request(pageid,current_time,(current_time -time_constant))
			current_time = current_time - time_constant
			page_feed = page_feed + initial_data
		except KeyError:
			break
	return page_feed


def run():
	db = MongoClient().db.fb_locations
	feed_db = MongoClient().db.page_feed
	for record in db.find():
		pageid = record['page_node']
		page_feed = get_page_daily_feed(pageid)
		#print page_feed
		entry = {
			"pageid" : pageid,
			"feed" : page_feed
		}
		#print "success"
		feed_db.insert_one(entry)
		break

run()







