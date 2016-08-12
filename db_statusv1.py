from pymongo import MongoClient
def somemethod():
    db = MongoClient ().db.user_media
    crsr = db.find ()

    count = 0
    c = 0

    for a in crsr:
        try:
            c += 1
            count += len (a['user_media'])
        except KeyError:
            continue
    print "doc", c
    print "er", count

def get_feed_count(value):
    db = MongoClient().db.page_feed

    token = []
    token_value = []
    count = 0
    for a in db.find():
        if a['pageid'] not in token:
            token.append(a['pageid'])
            token_value.append(count)
        else:
            try:
                token_value[token.index(a['pageid'])] += len(a['feed'][0])
            except IndexError:
                continue
    #i = 0
    #for a in token:
        #print a , token_value[i]
        #i+=1
    total_count= 0
    for a in token_value:
        total_count+=a
    print "total_feed",total_count
    if value == "all":
        print "pages extracted = ", len(token)
        print "total feed extracted= ", total_count
    else:
        pageid = raw_input("Please enter the name of the page:")
        if pageid in token:
            print "total feed extracted: " , token_value[token.index(pageid)]
        else:
            reply = raw_input("Cannot find the page please enter a new page ID?")
            while(reply != "quit" or reply != "Quit"):
                reply = raw_input("pageid:")
                if reply in token:
                    print "total feed extracted: ", token_value[token.index (reply)]
                else:
                    continue




