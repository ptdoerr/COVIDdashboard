import os
import pymongo
import matplotlib.pyplot as plt
import io

class MongoDbUtilities:

    def __init__(self, config: dict) -> None:
        self.config = config
        self.mongodb_user = os.environ.get('MONGO_DB_USER') #config['user']
        self.mongodb_password = os.environ.get('MONGO_DB_PASSWORD') #config['password']
        
    def connect_to_db():
        client = pymongo.MongoClient("mongodb+srv://" +self.mongodb_user +":" +self.mongodb_password +"@cluster0.yu9l6.mongodb.net/myFirstDatabase?retryWrites=true&w=majority") # server_api=ServerApi('1'))
        self.db = client.covid_dash
    
        return self.db
    
    def write_image_to_db(db, figure, date):
        img_buf = io.BytesIO()
        figure.savefig(img_buf, format='jpg')
        db.insert_one()