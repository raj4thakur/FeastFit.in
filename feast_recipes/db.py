from pymongo import MongoClient

# MongoDB connection setup
client = MongoClient('mongodb://localhost:27017/')  # Update with your MongoDB URI
db = client['FeastFit_DataBase']  # Replace with your database name

# Export the collections you'll use
interactions_collection = db['feast_recipes_recipeinteraction']  # Replace with your recipes collection name
accounts_collection=db['accounts_profile']
