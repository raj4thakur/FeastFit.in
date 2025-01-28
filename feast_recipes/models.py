from django.db import models
from django.conf import settings

# Recipe Model
class Recipe(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    procedure = models.TextField(help_text="Step-by-step instructions for preparing the dish.")
    cuisine = models.CharField(max_length=50)
    diet_type = models.CharField(max_length=50)
    preparation_time = models.PositiveIntegerField(help_text="Time in minutes")
    cooking_time = models.PositiveIntegerField(help_text="Time in minutes")
    servings = models.PositiveBigIntegerField(default=3, help_text='Ex-3,4,7')
    ingredients = models.TextField(help_text="List of ingredients separated by commas")
    allergens = models.TextField(blank=True, null=True, help_text="List any allergens")
    calories = models.PositiveIntegerField(blank=True, null=True)
    fat = models.FloatField(blank=True, null=True)
    protein = models.FloatField(blank=True, null=True)
    carbs = models.FloatField(blank=True, null=True)
    views = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0.0)
    total_reviews = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    image = models.ImageField(upload_to='recipe_images/', blank=True, null=True)
    saved = models.IntegerField(default=0)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_recipes'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def update_average_rating(self):
        total_ratings = self.ratings.count()
        if total_ratings > 0:
            self.average_rating = sum(r.rating for r in self.ratings.all()) / total_ratings
        else:
            self.average_rating = 0
        self.save()

    def __str__(self):
        return self.title


# Recipe Interaction Model
class RecipeInteraction(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='interactions'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='interactions'
    )
    liked = models.BooleanField(default=False)
    saved = models.BooleanField(default=False)
    shared = models.BooleanField(default=False)

    def toggle_like(self):
        if self.liked:
            self.liked = False
            self.recipe.likes -= 1
        else:
            self.liked = True
            self.recipe.likes += 1
        self.recipe.save()
        self.save()

    def toggle_save(self):
        self.saved = not self.saved
        self.save()

    def __str__(self):
        return f"{self.user} - {self.recipe} ({'Liked' if self.liked else 'Not Liked'})"


# Recipe Rating Model
class RecipeRating(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rating by {self.user} on {self.recipe.title}"
