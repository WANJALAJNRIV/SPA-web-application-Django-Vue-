from django import forms
from .models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm



class SignUpForm(UserCreationForm):
    class Meta:
            model = User
            fields = ['username', 'first_name', 'last_name', 'profile_image', 'date_of_birth', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    password = forms.CharField(widget=forms.PasswordInput)
