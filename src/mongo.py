""" Paquete para la conexion con la base de datos de mongo """
from pymongo import MongoClient
from bson import ObjectId

# from encoder import JSONEncoder

MONGO_COLLECTION = 'movies'

class MongoManager():
    MONGO_URL = "mongodb://localhost:27017/"
    MONGO_DB_NAME = "MoviePlatform"
    db: MongoClient

    def __init__(self) -> None:
        client = MongoClient(self.MONGO_URL)
        self.db = client[self.MONGO_DB_NAME]

    def valid_collection(self, collection):
        return collection in self.db.list_collection_names()

    @staticmethod
    def insert_film(movie) -> bool:
        """ Insert document in movies collection """
        mongo_manager = MongoManager()
        if not mongo_manager.db.valid_collection(MONGO_COLLECTION):
            return False
        mongo_manager.db.movies.insert_one(movie)

    @staticmethod
    def find_movies(title:str=None, director:str=None, year:int=None, score:int=None) -> list:
        """ Query the movies that satisfies the filters """
        mongo_manager = MongoManager()
        movies = []
        if not mongo_manager.valid_collection(MONGO_COLLECTION):
            return movies
        query = {}
        if title:
            query['title'] = {'$regex': title}
        if director:
            query['director'] = {'$regex': director}
        if year:
            query['year'] = year
        if score:
            query['score'] = score

        return mongo_manager.db[MONGO_COLLECTION].find(query)

    @staticmethod
    def update_movie(_id:str, title:str=None, director:str=None, year:int=None, score:int=None) -> bool:
        mongo_manager = MongoManager()
        if not mongo_manager.valid_collection(MONGO_COLLECTION):
            return False
        query = {}
        if title:
            query['title'] = title
        if director:
            query['director'] = director
        if year:
            query['year'] = year
        if score:
            query['score'] = score
        result = mongo_manager.db[MONGO_COLLECTION].update_one({'_id':ObjectId(_id)}, {'$set':query})
        return result.acknowledged

    @staticmethod
    def insert_movie(title, director, year, score) -> bool:
        mongo_manager = MongoManager()
        # not validate any kind of data because could be more than one film with the same title
        data = {
            'title':title,
            'director':director,
            'year':year,
            'score':score
        }
        result = mongo_manager.db[MONGO_COLLECTION].insert_one(data)
        return result.acknowledged
        

    @staticmethod
    def delete_movie(_id:str) -> bool:
        mongo_manager = MongoManager()
        data = {'_id': ObjectId(_id)}
        result = mongo_manager.db[MONGO_COLLECTION].delete_one(data)
        return result.acknowledged
