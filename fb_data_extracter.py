from pymongo import MongoClient
import requests
import time
from threading import Thread
import threading
import Queue


# database initialization
access_token = "EAACNrjHuFp0BAHJE4Nscd2gZCSu8CMMzmnlraqlcukZAEvQx6QIZCY8WYNylsm3ZAZCbl7Ms05eUoZAKzdEHZAT49DeQl2xDlR1DZALfujBXtRo27wywZAj664kb5ecOuia2uAJHcBKd7HMzdSQnuEjT1yxfHZADivCZCEZD"

def paginator(next_url, queb):
    data = []
    while (True):
        print "started paginating"
        try:
            dump = requests.get (next_url)
            feed = dump.json ()
            if (len (feed['data']) == 0):
                break

            queb.put (feed['data'])
            #print feed['data']
            # print data
        except KeyError:
            break
    print "finished paginating"
    return


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
        data_queue.put(data['data'])
        print "contact made"

    # print data
    except KeyError:
        return ["N/A"]
    # #print "here2"
    try:
        print "paginating initial query"
        paginator (data['paging']['next'], data_queue)
    except KeyError:
        return
    return


def get_page_feed(pageid):
    data_stream = Queue.Queue()
    current_time = int (time.time ())
    c = 7776000
    dstream = [Thread (target=feed_requestv1, args=[pageid, x, x - c, data_stream]) for x in range(current_time, 1388534400, -7776000)]
    c = 0
    for worker in dstream:
        print "started worker",c

        worker.start ()
    print "queue flush system has been switched on"
    bran = Thread(target=drain_timer, args=(data_stream, pageid,))
    bran.start()
    for worker in dstream:
        worker.join ()

    bran.join()
    print "thread_terminating"
    data_stream.task_done()
    print "memory is cleared"
    return 0


def drainer(queb, pageid):
    strain = []
    feed_db = MongoClient().db.page_feed
    if (queb.empty()):
        print "cannot flush queue, its empty"
        return 1
    # print "flushing queue"
    while not queb.empty():

        strain.append (queb.get ())

        # print strain
        print queb.empty()
        entry = {"pageid": pageid, "feed": strain}
        feed_db.insert_one (entry)
        strain = []
        print "queue is flushed"
    return 0


        # entry = { "pageid": pageid,"feed":strain}
        # eed_db.insert_one(entry)


def drain_timer(queb, pageid):
    global_count = 0
    df = 0
    while (threading.enumerate () > 1):
        drf = drainer (queb, pageid)
        time.sleep (1)
        print "started flushing queue"
        df +=drf
        if drf== 0:
            df =0
        if df >20:
            print "drainer has exited"
            return



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
        # pageid = record['page_node']
    page_feed = get_page_feed (pageid)
    print "completed extractions of ",pageid
    if( page_feed == 0):
        return
        # #print page_feed
        # entry = {
        # E "pageid": pageid,
        # "feed": page_feed
        # }#
        # #print "success"
        # feed_db.insert_one (entry)



if __name__ == '__main__':
    import thread

    locations = []
    for a in MongoClient ().db.fb_locations.find ():
        locations.append (a['page_node'])

    for a in locations:
        done = ["levelshkv", "KittySu.Delhi","MoonshineCafeBar"]
        if a in done:
            continue
        print "started extraction of " , a
        t = Thread (target=run1, args=(a,))
        t.start ()
        t.join ()
