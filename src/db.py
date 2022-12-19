from bson import ObjectId
from pymongo import MongoClient

client = MongoClient("localhost", 27017)


class DB:
    db = client['db2']
    collection = db['col2']

    @classmethod
    def insert_many(cls, data: list):
        res = cls.collection.insert_many(data)
        return res.acknowledged

    @classmethod
    def update_data(cls, _id: str, data: dict):
        _id = ObjectId(_id)
        query = {"_id": _id}
        _set = {"$set": data}
        res = cls.collection.update_one(query, _set)
        return res.acknowledged

    @classmethod
    def get_detail_null_documents(cls, limit=30):
        res = cls.collection.find({"detail": None}).limit(limit)
        return res if res else list()
