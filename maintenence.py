
from pymongo.errors import OperationFailure

class project_db:

    def __init__(self,db_assigned,MongoClient_Custom):



        self.host = '104.197.108.172'
        self.client = MongoClient_Custom(self.host)

        try:
            status = self.client[db_assigned].authenticate('accountUser1','password',mechanism='SCRAM-SHA-1')
            self.db = self.client[db_assigned]
        except OperationFailure:
            while (True):
                take_input = raw_input("Database Authentication Failed Try Again?")
                if (take_input == "Y" or take_input == "y"):
                    self.user_name = raw_input("User_name: ")
                    self.password = raw_input("Password: ")
                    #self.host=raw_input("Host Address : ")
                    db_name = raw_input("Name of Database: ")

                    try:
                        status = self.client[db_name].authenticate ('user_name', 'password', mechanism='SCRAM-SHA-1')
                    except OperationFailure:
                        continue
                    break

                else:
                    break

        print "Database Authentication Successful"
from pymongo import MongoClient as tree
db = project_db("db",tree)

from pymongo import MongoClient as man
ddb = project_db("admin",tree)