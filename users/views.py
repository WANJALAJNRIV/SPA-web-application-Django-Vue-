from .forms import SignUpForm, LoginForm
from django.shortcuts import render, redirect
from django.contrib.auth import logout 
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login, authenticate
import json


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'authentication/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Generate JWT token
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # Encode user details as a JSON object
            user_details = {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'access_token': access_token
            }
            user_details_json = json.dumps(user_details)
            redirect_url = f'/login/successful/#{user_details_json}'
            # redirect_url = f'http://localhost:5173/login/successful/#{user_details_json}'
            return redirect(redirect_url)
    else:
        form = LoginForm()

    return render(request, 'authentication/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')
