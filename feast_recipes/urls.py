from django.urls import path
from . import views

app_name = "feast_recipes"

urlpatterns = [
    path('', views.recipes, name='recipes'),
    path('search/', views.recipes, name='recipe_search'),
    path('upload/', views.upload_recipe, name='upload_recipe'),
    path('recipe/<int:recipe_id>/', views.recipe_content, name='recipe_content'),
    path('like/<int:recipe_id>/', views.like_recipe, name='like_recipe'),
    path('save/<int:recipe_id>/', views.save_recipe, name='save_recipe'),
    path('view/<int:recipe_id>/', views.increment_view_count, name='view_recipe'),
]
