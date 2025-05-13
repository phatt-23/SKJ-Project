from django.http import Http404, HttpRequest
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from django.contrib.auth import get_user_model

User = get_user_model()

def login_view(request: HttpRequest):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'registration/login.html')


def register_view(request: HttpRequest):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
       
        valid_state = True

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            valid_state = False 

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            valid_state = False 

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already taken.')
            valid_state = False 

        if valid_state:
            user = User.objects.create_user(username=username, email=email, password=password1)
            login(request, user)
            return redirect('dashboard')

    return render(request, 'registration/register.html')


def logout_view(request: HttpRequest):
    if request.method == 'POST':
        logout(request)
        return redirect('login')

    return render(request, 'registration/logout.html')





