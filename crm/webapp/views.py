from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegistrationForm, AddClientForm
from . models import Client, Product
from django.core.mail import send_mail
from .forms import AddProductForm


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


def client(request, pk):
    if request.user.is_authenticated:
        # look up specific client data from the database
        client_record = Client.objects.get(id=pk)
        return render(request, 'client.html', {'client_record': client_record})
    else:
        messages.success(request, 'You need to login first')
        return redirect('home')


def client_delete(request, pk):
    if request.user.is_authenticated:
        delete_record = Client.objects.get(id=pk)
        delete_record.delete()
        messages.success(request, 'You have successfully deleted...')
        return redirect('home')
    else:
        messages.success(request, 'You have to login first')
        return redirect('home')
    
    
def add_client(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = AddClientForm(request.POST)
            if form.is_valid():
                add_client = form.save()
                messages.success(request, 'New client added...')
                return redirect('home')
            # If form is not valid, we'll fall through to render with the form containing errors
        else:
            form = AddClientForm()  # Create a blank form for GET requests
        
        return render(request, 'add_client.html', {'form': form})
    else:
        messages.success(request, 'You have to log in to add new record...')
        return redirect('home')


def client_update(request, pk):
    if request.user.is_authenticated:
        current_record = Client.objects.get(id=pk)
        form = AddClientForm(request.POST or None, instance=current_record)
        if request.method == 'POST':
            if form.is_valid():
                update_client = form.save()
                messages.success(request, 'Client info updated...')
                return redirect('home')
        return render(request, 'client_update.html', {'form': form})
    else:
        messages.success(request, 'You have to login...')
        return redirect('home')
    
# for Product 
def products_purchased(request, pk):
    if request.user.is_authenticated:
        client = get_object_or_404(Client, id=pk)
        products = Product.objects.filter(client=client)
        return render(request, 'products.html', {'client': client, 'products': products})
    else:
        messages.error(request, 'You need to log in to view purchases...')
        return redirect('home')
    


def add_product(request, client_id):
    client = Client.objects.get(id=client_id)
    if request.method == 'POST':
        form= AddProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.client = client
            product.save()

            # Send mail
            subject = 'Thank You fo rYour Purchase!'
            send_mail(subject, messages, "Product purchase added and email sent!")
            return redirect('products_purchased', pk=client.id)
    else:
        form = AddProductForm()
    return render(request, 'add_product.html', {'form': form, 'client': client})



#  add product view function
def add_product(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully')
            return redirect('home')
    else:
        form = AddProductForm()
    return render(request, 'add_product.html', {'form': form})


# Inventory view function
def inventory(request):
    products = Product.objects.all()
    return render(request, 'inventory_html', {'products': products})

