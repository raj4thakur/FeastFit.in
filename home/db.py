from pymongo import MongoClient

# MongoDB connection setup
client = MongoClient('mongodb://localhost:27017/')  # Update with your MongoDB URI
db = client['FeastFit_DataBase']  # Replace with your database name

# Export the collections you'll use
recipes_collection = db['feast_recipes_recipe']  # Replace with your recipes collection name
users_profiles=db['accounts_profile']