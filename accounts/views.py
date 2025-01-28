from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegistrationForm  # Ensure the form is imported
# from .models import User  # Import the custom user model

def login_view(request):
    error = None  # Initialize error variable
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home:home')  # Replace 'home:home' with your actual home URL name
        else:
            error = "Invalid email or password. Please try again."

    return render(request, 'accounts/login.html', {'error': error})


# Register View
def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Save the user and log them in
            user = form.save()
            login(request, user)  # Automatically log the user in after registration
            messages.success(request, 'Registration successful! Welcome to FeastFit.')
            return redirect('home:home')  # Redirect to the home page
        else:
            # Return the form with errors
            messages.error(request, 'Please fix the errors below.')
            return render(request, 'accounts/register.html', {'form': form})

    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})

# Logout View
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home:home')  # Redirect to home page


from django.contrib.auth.decorators import login_required
from .models import Profile, Diet, Recipe, MealPlan, SavedRecipe
from .forms import ProfileForm, ProfilePicForm, DietaryPreferencesForm

@login_required
def profile_view(request):
    # Ensure profile exists or create it dynamically
    profile, created = Profile.objects.get_or_create(user=request.user)

    # diets = Diet.objects.all()
    recipes = request.user.recipes.all()
    # saved_recipes = request.user.saved_recipes.all()
    # meal_plans = request.user.meal_plans.all()

    context = {
        'user': request.user,
        'profile': profile,
        # 'diets': diets,
        'recipes': recipes,
        # 'saved_recipes': saved_recipes,
        # 'meal_plans': meal_plans,
    }
    print(recipes)
    return render(request, 'accounts/profile.html', context)


from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from .forms import ProfileForm

@login_required
def update_profile(request):
    if request.method == 'POST':
        print("POST data:", request.POST)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Profile updated successfully!")
        else:
            print("Form errors:", profile_form.errors)  # Debugging: log form errors
            messages.error(request, "Error updating profile. Please check your inputs.")
        return redirect('accounts:profile')
    else:
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'accounts/profile.html', {'profile_form': profile_form})




@login_required
def upload_profile_pic(request):
    if request.method == 'POST':
        new_pic = request.FILES.get('new_profile_pic')
        if new_pic:
            request.user.profile.profile_pic = new_pic
            request.user.profile.save()
            messages.success(request, 'Profile picture updated successfully.')
        else:
            messages.error(request, 'Please select a valid image.')
        return redirect('accounts:profile') 


@login_required
def update_dietary_preferences(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        dietary_form = DietaryPreferencesForm(request.POST, instance=profile)
        if dietary_form.is_valid():
            dietary_form.save()
            messages.success(request, "Dietary preferences updated successfully!")
        else:
            messages.error(request, "Error updating dietary preferences.")
    return redirect('accounts:profile')


@login_required
def feedback(request):
    pass

def help_support(request):
    pass


def update_security_settings(request):
    pass