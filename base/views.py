from django.shortcuts import render, redirect
from .models import Car, Order
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
# Create your views here.

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        
        except:
            messages.error(request, "User account not found")

        user = authenticate(request, username=username, password =password) 

        if user is not None:
            login(request, user)
            if username == "rich-k-tech":
                return redirect('admin-page')
            else:
                return redirect('home-page')
        else:
            messages.error(request, "invalid password, please try again")       
    return render(request, "login.html")

@login_required(login_url='login/')
def index_view(request):
    approved_orders = Order.objects.filter(client=request.user, status="approved", is_active=True).count()

    # Get the values from the submitted form data
    q = request.GET.get('q')
    min_price = request.GET.get('minprice')
    max_price = request.GET.get('maxprice')

    # Query all cars that are available
    cars = Car.objects.filter(is_available=True)

    # Apply filtering based on 'q' if it exists
    if q:
        cars = cars.filter(name__icontains=q)

    # Apply filtering based on minimum and maximum prices
    if min_price:
        cars = cars.filter(price__gte=min_price)
    if max_price:
        cars = cars.filter(price__lte=max_price)

    # Filter orders by the logged-in user
    my_orders = Order.objects.filter(client=request.user)

    # Get the list of car IDs ordered by the logged-in user
    ordered_car_ids = my_orders.values_list('car__id', flat=True)

    # Exclude the cars ordered by the logged-in user
    cars = cars.exclude(id__in=ordered_car_ids)

    number_of_items = Order.objects.filter(client=request.user, is_active=False).count()

    context = {
        "cars": cars,
        "my_orders": my_orders,
        "approved": approved_orders,
        "number_of_items": number_of_items
    }
    return render(request, "cars.html", context)

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        try:
            user = User.objects.get(username=username)
        except:
            user = None    

        if user:
            messages.error(request, "please choose another username") 

        if password1 != password2:
            messages.error(request, "please provide matching passwords")  


        try:
            user = User.objects.create(
                username=username,
                password=make_password(password1),
                is_active=True,
                is_staff=True,
                email=f"{username}@gmail.com",
            )
            login(request, user)
            return redirect('home-page')
        except:
            messages.error(request, "something went wrong")
    return render(request, 'signup.html')

@login_required(login_url='login/')
def add_to_cart(request, pk):
    this_car = Car.objects.get(id =pk)
    Order.objects.create(
        car = this_car,
        client = request.user,
    )
    return redirect('home-page')    


@login_required(login_url="login/")    
def remove_from_cart(request, pk):
    order = Order.objects.get(car = pk, client=request.user)
    order.delete()
    return redirect('my-orders-page')    

@login_required(login_url="login/")    
def my_orders_view(request):
    approved_orders = Order.objects.filter(client=request.user, status="approved", is_active=True).count()

    orders = Order.objects.filter(client = request.user, is_active=False)
    cars = []
    total = 0
    for order in orders:
        cars.append(Car.objects.get(id = order.car.id))
        total += Car.objects.get(id = order.car.id).price
    context ={
        "number_of_items": orders.count(),
        "cars": cars,
        "total": total,
        "approved": approved_orders
    }

    return render(request, 'my_orders.html', context)

@login_required(login_url="login/")    
def order_all(request):
    orders = Order.objects.filter(client = request.user).update(is_active= True)
    for order in Order.objects.filter(client = request.user, is_active = True):
        Car.objects.get(id = order.car.id).is_available = False
    return redirect('order-history') 

@login_required(login_url="login/")    
def order_history(request):
    orders = Order.objects.filter(client = request.user, is_active=False)
    selected_items = Order.objects.filter(client = request.user, is_active=True)
    approved_orders = Order.objects.filter(client=request.user, status="approved", is_active=True).count()
    for order in selected_items:
        order.cars = list()
        order.cars.append(Car.objects.get(id = order.car.id))
        order.total =0
        order.total += Car.objects.get(id = order.car.id).price
    context ={
        "number_of_items": orders.count(),
        "orders" : selected_items,
        "approved": approved_orders
    }
    
    return render(request, 'order-history.html', context)    


def logout_view(request):
    logout(request)
    return redirect('login-page')

@login_required(login_url="login/")    
def admin_view(request):
    cars = Car.objects.all()
    sold_cars = Car.objects.filter(is_available=False)
    instock_cars = Car.objects.filter(is_available=True)
    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        image = request.FILES.get("image")
        speed = request.POST.get("speed")
        try:
            Car.objects.create(
            name=name,
            price=price,
            image = image,
            speed= speed
            )
        except:
            messages.error(request, "something went wrong")    
        return redirect('admin-page')
    context={
        "is_admin": True,
        "total": cars.count(),
        "sold": sold_cars.count(),
        "instock": instock_cars.count()
    }
    return render(request, 'admin.html', context)

@login_required(login_url="login/")    
def orders_view(request):
    orders = Order.objects.filter(is_active=True, status="pending")
    context ={
            "is_admin": True,
            "orders": orders
    }
    return render(request, "orders.html", context)

@login_required(login_url="login/")    
def reject(request, pk):
    Order.objects.get(id =pk).delete()
    return redirect('orders-page')

@login_required(login_url="login/")    
def approve(request, pk):
    Order.objects.filter(id =pk).update(status = "approved")
    return redirect('orders-page')
@login_required(login_url="login/")    
def history_view(request):
    orders = Order.objects.all()
    context ={
        "is_admin": True,
        "orders": orders
    }
    return render(request, 'orders-history.html', context)

    



   

