from pymongo import MongoClient as MongoClient1

host = '104.197.108.172'
client = MongoClient1(host)
user_name= raw_input("username :")
password = raw_input("password :")
client.db.authenticate(user_name,password,mechanism='SCRAM-SHA-1')

class crawler_file:
    def __init__(self,file_path):
        #opening the file and reading it
        file_stream = open(file_path,mode='r')
        headers = file_stream.readline()
        stream = file_stream.readlines()
        file_stream.close()
        headers = headers.split("\t")
        self.export = []
        for line in stream:
            entry = {}
            line = line.split("\t")
            i=0
            for header in headers:
                entry[header] = line[i]
                i+=1
            self.export.append(entry)
    def data_export(self,database):
        for record in self.export:
            database.insert_one(record)
#Example
#strollup = "C:\Users\Anshita Aggarwal\strolluptab.txt"
#export_to_mongo = crawler_file(strollup).data_export(MongoClient().db['crawler_strollup'])