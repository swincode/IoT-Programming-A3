
import datetime, json
from pymongo import MongoClient

DB_URI = "mongodb://localhost:something"

client = MongoClient(DB_URI)

db = client["data"]

class Mongo:

    def __init__(self):
        self.db = db
    
    def insert_data(self, x: int, y: int):
        self.db.insert_one({
            x_coord = x,
            y_coord = y,
            frame = "something not implemented",
            time = datetime.datetime.now()
        })

    def get_latest(self):
        res = self.db.find().sort({"time": -1}).limit(1)[0]
        res["time"] = res["time"].strftime("%d-%b-%Y %H:%M:%S")
        return json.dumps(res)

