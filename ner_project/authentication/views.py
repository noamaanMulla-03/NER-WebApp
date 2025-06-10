from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

def login_view(request):
    # If user is already logged in, redirect to upload
    if request.user.is_authenticated:
        return redirect('upload')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('upload')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

def register_view(request):
    # If user is already logged in, redirect to upload
    if request.user.is_authenticated:
        return redirect('upload')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! Please log in.')
            return redirect('login')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    # Log out the user and redirect to login page
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')