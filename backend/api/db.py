import pymongo
from pymongo import MongoClient


class DataBase:

    def __init__(self):

        client = MongoClient('mongo', 27017)
        db = client.images_db
        self.images = db.images

    def add_image(self, id, image):
        self.images.insert_one({"id": id,
                                "image": image,
                                })
