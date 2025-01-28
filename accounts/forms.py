from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

class RegistrationForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your username', 'class': 'input-field'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email address', 'class': 'input-field'})
    )
    country = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your country', 'class': 'input-field'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password', 'class': 'input-field'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password', 'class': 'input-field'})
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise ValidationError("Passwords do not match")

        email = cleaned_data.get("email")
        if get_user_model().objects.filter(email=email).exists():
            raise ValidationError("Email is already registered.")
        return cleaned_data

    def save(self):
        user = get_user_model().objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        user.country = self.cleaned_data['country']
        user.save()
        return user



from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'gender', 'birthdate', 'country']
    def clean_caloric_goals(self):
        caloric_goals = self.cleaned_data.get('caloric_goals')
        if caloric_goals < 1200 or caloric_goals > 5000:  # Example range
            raise forms.ValidationError("Caloric goals must be between 1200 and 5000.")
        return caloric_goals

class ProfilePicForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic']

class DietaryPreferencesForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['preferred_diet', 'allergies', 'caloric_goals']




