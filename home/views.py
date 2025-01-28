from django.shortcuts import render
from .db import recipes_collection, users_profiles  # Import the MongoDB collections

def home(request):
    # Fetch recipes from MongoDB
    recipes = list(recipes_collection.find().limit(8))  # Convert cursor to list for Django templates
    for recipe in recipes:
        recipe['_id'] = str(recipe['_id'])  # Convert ObjectId to string for JSON serialization
    print("Got recipes for home template!")

    # Fetch profile picture for the logged-in user
    user_profile_pic = None
    if request.user.is_authenticated:
        # Find the profile associated with the logged-in user
        user_profile = users_profiles.find_one({'user_id': request.user.id})
        if user_profile and 'profile_pic' in user_profile:  # Ensure 'profile_pic' key exists
            user_profile_pic = user_profile['profile_pic']
    return render(request, 'home/home.html', {
        'recipes': recipes,
        'profile_pic': user_profile_pic,  # Pass profile picture to template
    })
