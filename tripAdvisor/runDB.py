from DB import DB

db=DB()
def main():
    print()
    db.connectToDB("tripAdvisor")

    #db.db["poi"].update_many({"name":"蘭陽博物館"},{"$set": {"type": ""}})
    pipe=[
    {
     '$group':{
         '_id':"$poi_id",
         'count':{'$sum':1}
         }
    },{
     '$sort':{"count":-1}}
]
    result=db.db["review"].aggregate(pipeline=pipe)
    count=0
    for doc in result:
        print(doc["count"])
        count+=1
    print(count)

if __name__ == "__main__":
    main()





