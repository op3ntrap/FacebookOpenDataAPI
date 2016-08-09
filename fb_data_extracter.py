from pymongo import MongoClient
import requests
import time
from threading import Thread
import threading
import Queue
from thread import start_new_thread

# database initialization
access_token = "EAACNrjHuFp0BAPdpmSRZAB7BgvU3Khjzf0YPZBZChfOZC8XOHHpeHckXof6NzbJL1VO0hWL55ZAF53SdKBUxazakzbWWSHzZBBnbEpsW6ZA4PWmfeFU8ikJjL4ZCKZBuSgAz6CrggagkXPhV2tebLUZBimtLSwUCJ4bfYZD"


def paginator(next_url, queb):
    data = []
    while (True):
        # print "executed"
        try:
            dump = requests.get (next_url)
            feed = dump.json ()
            if (len (feed['data']) == 0):
                break

            queb.put (feed['data'])
            # print data
        except KeyError:
            break


'''
# feed datarequest
def feed_request(pageid, until, since):
    # print "executed"
    try:
        data_request = requests.get (
            "https://graph.facebook.com/v2.7/" + str (pageid) + "/feed?limit=100&since=" + str (
                since) + "&until=" + str (until) + "&access_token=" + access_token)
        data = data_request.json ()

        queb.put (data['data'])
        # print data
    except KeyError:
        return None
    # print "here2"
    paginator (data['paging']['next'])

    return final_data

'''


def feed_requestv1(pageid, until, since, data_queue):
    # print "executeda"
    try:
        data_request = requests.get (
            "https://graph.facebook.com/v2.7/" + str (pageid) + "/feed?limit=100&since=" + str (
                since) + "&until=" + str (until) + "&access_token=" + access_token)
        data = data_request.json ()
        if (len (data['data']) == 0):
            return
        data_queue.put (data['data'])

    # print data
    except KeyError:
        return ["N/A"]
    # #print "here2"
    try:
        paginator (data['paging']['next'], data_queue)
    except KeyError:
        return
    return


def get_page_feed(pageid):
    data_stream = Queue.Queue ()
    current_time = int (time.time ())
    c = 7776000
    dstream = [Thread (target=feed_requestv1, args=[pageid, x, x - c, data_stream]) for x in
               range (current_time, 1388534400, -7776000)]

    for worker in dstream:
        worker.start ()

    start_new_thread (drain_timer, (data_stream, pageid,))

    for worker in dstream:
        worker.join ()

    page_feed = []
    while not data_stream.empty ():
        page_feed.append (data_stream.get ())
    data_stream.join ()
    return page_feed


def drainer(queb, pageid):
    strain = []
    feed_db = MongoClient ().db.page_feed
    # print "flushing queue"

    while not queb.empty ():
        strain.append (queb.get ())
        # print strain
        entry = {"pageid": pageid, "feed": strain}
        feed_db.insert_one (entry)
        strain = []


        # entry = { "pageid": pageid,"feed":strain}
        # eed_db.insert_one(entry)


def drain_timer(queb, pageid):
    while (threading.enumerate () > 1):
        drainer (queb, pageid)
        time.sleep (3)


'''
def get_page_daily_feed(pageid):
    page_feed = []
    current_time = time.time ()
    time_constant = 86400
    current_time = int (time.time ())
    while (current_time > 0):
        try:
            # print "here"
            initial_data = feed_request (pageid, current_time, (current_time - time_constant))
            current_time = current_time - time_constant
            page_feed = page_feed + initial_data
        except KeyError:
            break
    return page_feed


def run():
    db = MongoClient ().db.fb_locations
    feed_db = MongoClient ().db.page_feed
    for record in db.find ():
        pageid = record['page_node']
        page_feed = get_page_daily_feed (pageid)
        # #print page_feed
        entry = {
            "pageid": pageid,
            "feed": page_feed
        }
        # #print "success"
        feed_db.insert_one (entry)
        break

'''
def run1(pageid):
    db = MongoClient ().db.fb_locations
    feed_db = MongoClient ().db.page_feed
    for record in db.find ():
        # pageid = record['page_node']
        page_feed = get_page_feed (pageid)
        # #print page_feed
        # entry = {
        # E "pageid": pageid,
        # "feed": page_feed
        # }#
        # #print "success"
        # feed_db.insert_one (entry)
        break




if __name__ == '__main__':
    import thread
    locations = {}
    for a in MongoClient ().db.fb_locations.find ():
        thread.start_new_thread (run1,(a,))
        time.sleep (900)
