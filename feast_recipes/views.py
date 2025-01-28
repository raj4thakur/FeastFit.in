from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Recipe
from pymongo import MongoClient

def recipes(request):
    recipes_query = Recipe.objects.all()
    search = request.GET.get('search', '')
    if search:
        recipes_query = recipes_query.filter(title__icontains=search)
    cuisine = request.GET.get('cuisine', '')
    if cuisine:
        recipes_query = recipes_query.filter(cuisine__iexact=cuisine)
    ingredient = request.GET.get('ingredient', '')
    if ingredient:
        recipes_query = recipes_query.filter(ingredients__icontains=ingredient)
    diet = request.GET.get('diet', '')
    if diet:
        recipes_query = recipes_query.filter(diet_type__iexact=diet)
    paginator = Paginator(recipes_query, 8) 
    page_number = request.GET.get('page')
    all_recipes = paginator.get_page(page_number)

    client = MongoClient('mongodb://localhost:27017/') 
    db = client['FeastFit_DataBase'] 
    users_profiles=db['accounts_profile']
    user_profile_pic = None
    if request.user.is_authenticated:
        # Find the profile associated with the logged-in user
        user_profile = users_profiles.find_one({'user_id': request.user.id})
        if user_profile and 'profile_pic' in user_profile:  
            user_profile_pic = user_profile['profile_pic']
    recipe_profiles = []
    for recipe in all_recipes:
        user_profile = users_profiles.find_one({'user_id': recipe.created_by_id})
        if user_profile:
            recipe_profiles.append({
                'recipe_id': recipe.id,
                'username': user_profile.get('full_name'),
                'profile_pic': user_profile.get('profile_pic'),
            })
    context = {
        'all_recipes': all_recipes,
        'profile_pic': user_profile_pic,
        'recipe_profiles': recipe_profiles,
    }
    return render(request, 'feast_recipes/recipes.html', context)

from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Recipe

def upload_recipe(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        procedure = request.POST.get('procedure')
        cuisine = request.POST.get('cuisine')
        diet_type = request.POST.get('diet_type')
        ingredients = request.POST.get('ingredients')
        allergens = request.POST.get('allergens', '')
        prep_time = request.POST.get('prep_time')
        cook_time = request.POST.get('cook_time')
        servings = request.POST.get('servings')
        image = request.FILES.get('image')
        calories = request.POST.get('calories', None)
        protein = request.POST.get('protein', None)
        fat = request.POST.get('fat', None)
        carbs = request.POST.get('carbs', None)
        # Ensure the user is authenticated
        if not request.user.is_authenticated:
            messages.error(request, "You need to be logged in to upload a recipe.")
            return redirect('accounts:login')  # Redirect to login page if user is not authenticated
        # Save to the database
        recipe = Recipe(
            title=title,
            description=description,
            procedure=procedure,
            cuisine=cuisine,
            diet_type=diet_type,
            ingredients=ingredients,
            allergens=allergens,
            preparation_time=prep_time,
            cooking_time=cook_time,
            servings=servings,
            image=image,
            calories=calories,
            protein=protein,
            fat=fat,
            carbs=carbs,
            created_by=request.user  # Use the logged-in user for created_by
        )

        recipe.save()
        messages.success(request, "Recipe uploaded successfully!")
        return redirect('home:home')  # Redirect to a list of recipes or another appropriate page
    return render(request, 'feast_recipes/upload_recipe.html',)


from django.conf import settings
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Recipe  # Assuming you have a Recipe model in your Django app
def recipe_content(request, recipe_id):
    # Fetch the recipe from the database using the recipe ID
    recipe = get_object_or_404(Recipe, id=recipe_id)
    # Increment the view count by 1 each time the recipe page is accessed
    recipe.views += 1
    recipe.save()
    # Pre-process the data
    recipe.steps = recipe.procedure.split("\r\n")
    recipe.ingredients_list = recipe.ingredients.split("\r\n")
    recipe.allergens_list = recipe.allergens.split(", ")
    # Return the recipe to be rendered in the template
    return render(request, 'feast_recipes/recipe_content.html', {'recipe': recipe, 'MEDIA_URL': settings.MEDIA_URL})


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .db import interactions_collection  # Your MongoDB interactions collection

@csrf_exempt
def like_recipe(request, recipe_id):
    if request.method == "POST" and request.user.is_authenticated:
        user_id = request.user.id

        # Parse the JSON body
        body = json.loads(request.body)
        is_liked = body.get("is_liked", False)

        # Interactions collection for tracking user likes
        interaction = interactions_collection.find_one({"user_id": user_id, "recipe_id": recipe_id})

        if interaction and interaction.get("liked", False):
            # Unlike the recipe
            interactions_collection.delete_one({"user_id": user_id, "recipe_id": recipe_id})
            is_liked = False
        else:
            # Like the recipe
            interactions_collection.update_one(
                {"user_id": user_id, "recipe_id": recipe_id},
                {"$set": {"liked": True}},
                upsert=True
            )
            is_liked = True

        # Update the like count in the recipes collection
        if is_liked:
            recipes_collection.update_one({"_id": recipe_id}, {"$inc": {"likes": 1}})
        else:
            recipes_collection.update_one({"_id": recipe_id}, {"$inc": {"likes": -1}})

        # Get the updated like count
        recipe = recipes_collection.find_one({"_id": recipe_id})
        likes_count = recipe.get("likes", 0)

        return JsonResponse({"likes": likes_count, "is_liked": is_liked})

    return JsonResponse({"error": "Unauthorized"}, status=403)



def increment_view_count(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    recipe.increase_views()
    return JsonResponse({'status': 'success', 'views': recipe.views})


def save_recipe():
    pass