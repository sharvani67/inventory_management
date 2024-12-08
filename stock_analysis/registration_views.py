from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Registration View
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
            else:
                User.objects.create_user(username=username, password=password)
                messages.success(request, 'Registration successful.')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match.')
    return render(request, 'registration/register.html')

# Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Replace 'home' with your desired view name
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'registration/login.html')

# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')
