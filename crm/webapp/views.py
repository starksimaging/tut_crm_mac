from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegistrationForm
from . models import Client

# Create your views here.
def home(request):
# Grab all client records from the database
    clients = Client.objects.all()

    # check if the user is logged in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # authenticate the user
        user = authenticate(request, username=username, password=password)

        # if the user is authenticated
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been logged in successfully')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('home')
    else:
        return render(request, 'home.html', {'clients': clients})   # add the clients in quotation marks then pass the clients reference with the clients variable
                                                                    # through this we will send all the client data to the home page.



# This function is used to authenticate the user and log them in.
# this function we will use if we want to use any seperate login page.
# def login_view(request):
#     pass

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('home') 


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Account created for {username}')
            return redirect('home')
    else:
        form = RegistrationForm()
    
    return render(request, 'register.html', {'form': form})


