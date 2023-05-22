from django.shortcuts import render, redirect
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Car

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Car

@login_required(login_url='login')
def HomePage(request):
    if request.method == 'POST':
        # Создание новой машины
        if 'create_car' in request.POST:
            name = request.POST['name']
            description = request.POST['description']
            price = request.POST['price']
            photo = request.FILES['photo']
            Car.objects.create(name=name, description=description, price=price, photo=photo)
            return redirect('home')

        # Удаление машины
        if 'delete_car' in request.POST:
            car_id = request.POST['car_id']
            Car.objects.filter(id=car_id).delete()
            return redirect('home')

        # Редактирование машины
        if 'edit_car' in request.POST:
            car_id = request.POST['car_id']
            car = Car.objects.get(id=car_id)
            car.name = request.POST['name']
            car.description = request.POST['description']
            car.price = request.POST['price']
            if 'photo' in request.FILES:
                car.photo = request.FILES['photo']
            car.save()
            return redirect('home')

    # Получение списка всех машин
    cars = Car.objects.all()
    context = {'cars': cars}
    return render(request, 'Home.html', context)

# Define the CreateItem view function
def CreateItem(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        photo = request.FILES['photo']
        Car.objects.create(name=name, description=description, price=price, photo=photo)
        return redirect('home')
    else:
        return render(request, 'create_item.html')

# Define the UpdateItem view function
def UpdateItem(request, item_id):
    item = Car.objects.get(id=item_id)

    if request.method == 'POST':
        item.name = request.POST['name']
        item.description = request.POST['description']
        item.price = request.POST['price']
        if 'photo' in request.FILES:
            item.photo = request.FILES['photo']
        item.save()
        return redirect('home')

    context = {'item': item}
    return render(request, 'update_item.html', context)

# Define the DeleteItem view function
def DeleteItem(request, item_id):
    Car.objects.filter(id=item_id).delete()
    return redirect('home')

# Define the CreateItem view function
def CreateItem(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        photo = request.FILES['photo']
        Car.objects.create(name=name, description=description, price=price, photo=photo)
        return redirect('home')
    else:
        return render(request, 'create_item.html')

def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            return HttpResponse("Your password and confirm password are not the same!!")
        else:
            my_user = User.objects.create_user(uname, email, pass1)
            my_user.save()
            return redirect('login')

    return render(request, 'signup.html')

def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse("Username or Password is incorrect!!!")

    return render(request, 'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')
