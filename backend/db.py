from flask_pymongo import pymongo

mongo = pymongo.MongoClient(
    "mongodb+srv://felix:EqnC3r1QDq5pPuH3@todo.cmrraic.mongodb.net/?retryWrites=true&w=majority"
)

db = mongo.db
