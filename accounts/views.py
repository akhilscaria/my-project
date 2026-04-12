from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from utils.auth import api_login_required
from utils.api_client import APIClient
from config.api_config import LOGIN_URL

def login_view(request):
    if request.method == 'POST':
        data = {
            "username": request.POST.get('username'),
            "password": request.POST.get('password')
        }

        response = APIClient().post(LOGIN_URL, data)

        try:
            res = response.json()
            msg = res.get("message", "Login failed")
        except:
            msg = "Invalid API response"
            res = {}

        if response.status_code == 200 and res.get("status") == "success":
            #mark user as logged in
            request.session['is_authenticated'] = True
            #set session values
            request.session['username'] = res.get("username")
            request.session['userid'] = res.get("userid") 

            messages.success(request, msg)
            return redirect('home')
        else:
            messages.error(request, msg)

    return render(request, 'accounts/login.html')


@api_login_required
def home_view(request):
    return render(request, 'accounts/home.html')


@api_login_required
def profile_view(request):
    return render(request, 'customers/profile.html')


def logout_view(request):
    request.session.flush()
    return redirect('login')