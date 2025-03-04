from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegistrationForm, AddClientForm
from . models import Client, Product
from django.core.mail import send_mail
from .forms import AddProductForm
from django.db.models import Sum, Count

# Create your views here.
def home(request):
    # Grab all client records from the database
    clients = Client.objects.all()

    # Aggregate calculations
    total_revenue = Product.objects.aggregate(Sum('price'))['price__sum'] or 0
    total_clients = Client.objects.count()
    total_products_sold = Product.objects.count()

    # Check if the user is logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'You have been logged in successfully')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('home')
    
    # Render the homepage with aggregated sales data
    return render(request, 'home.html', {
        'clients': clients,
        'total_revenue': total_revenue,
        'total_clients': total_clients,
        'total_products_sold': total_products_sold
    })


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

            # Corrected send_mail function with all required arguments
            send_mail(
                subject,
                messages,
                "your_email@example.com",  # Replace with a valid sender email
                [client.email],  # The recipient list should be a list, even for one email
                fail_silently=False,  # (Optional) Raise error if email fails
            )

            return redirect('products_purchased', pk=client.id)
    else:
        form = AddProductForm()
    return render(request, 'add_product.html', {'form': form, 'client': client})



