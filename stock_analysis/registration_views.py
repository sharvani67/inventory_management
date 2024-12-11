from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import Profile  # Import Profile if you're using it
ROLE_CHOICES = [
    ('admin', 'Admin'),
    ('owner', 'Owner'),
    ('manager', 'Manager'),
]

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST.get('role')  # Get the role from the form
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
            else:
                user = User.objects.create_user(username=username, password=password)
                Profile.objects.create(user=user, role=role)  # Create Profile and associate with the user
                messages.success(request, 'Registration successful.')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match.')
    return render(request, 'registration/register.html', {'role_choices': ROLE_CHOICES})



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            try:
                role = user.profile.role  # Safely access the profile's role
                request.session['user_role'] = role
                request.session['user_name'] = username
                login(request, user)
                return redirect('home')
            except Profile.DoesNotExist:
                messages.error(request, "Profile does not exist. Please contact support.")
                return redirect('login')
        else:
            messages.error(request, "Invalid username or password")
            
    return render(request, 'registration/login.html')



def logout_view(request):
    logout(request)
    request.session.flush()  # Clear the session
    return redirect('login')
