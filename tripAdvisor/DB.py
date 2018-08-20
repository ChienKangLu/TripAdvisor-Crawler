from pymongo import MongoClient
class DB:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)

    def connectToDB(self,dbName):
        self.db = self.client[dbName]

    def findall(self,collection_name):
        return self.db[collection_name].find()

    def find(self,query,collection_name):
        for doc in self.db[collection_name].find(query):
            print(doc)
    def exit(self,name,collection_name):
        result=self.db[collection_name].find_one({"name":name})
        if result!=None:
            return True
        else:
            return False

    def insert(self,object,collection_name):
        result =self.db[collection_name].insert_one(object.__dict__)
        return result.inserted_id




