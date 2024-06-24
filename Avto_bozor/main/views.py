from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import HttpResponseRedirect

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .forms import CarForm, CommentForm, CustomUserCreationForm
from .models import Car, Brand, Comment

def index(request):
    cars = Car.objects.all()
    brands = Brand.objects.all()
    return render(request, 'main/index.html', {'cars': cars, 'brands': brands})

def car_detail(request, car_id):
    car = get_object_or_404(Car, pk=car_id)

    if request.user.is_authenticated:
        viewed_cars = request.session.get('viewed_cars', [])
        if car_id not in viewed_cars:
            car.views += 1
            car.save()
            viewed_cars.append(car_id)
            request.session['viewed_cars'] = viewed_cars

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.car = car
            comment.user = request.user
            comment.save()
            return HttpResponseRedirect(reverse('car_detail', args=[car_id]))
    else:
        form = CommentForm()

    comments = car.comments.all()
    similar_cars = Car.objects.filter(brand=car.brand).exclude(id=car_id)[:4]

    return render(request, 'main/detail.html', {
        'car': car,
        'comments': comments,
        'form': form,
        'similar_cars': similar_cars
    })

def brand_cars(request, brand_id):
    brand = get_object_or_404(Brand, pk=brand_id)
    cars = Car.objects.filter(brand=brand)
    return render(request, 'main/brand_cars.html', {'brand': brand, 'cars': cars})

@login_required
def create_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            car.owner = request.user
            car.save()
            return redirect('index')
    else:
        form = CarForm()
    return render(request, 'main/create_car.html', {'form': form})

@login_required
def update_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            return redirect('car_detail', car_id=car.id)
    else:
        form = CarForm(instance=car)
    return render(request, 'main/update_car.html', {'form': form})

@login_required
def delete_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if request.method == 'POST':
        car.delete()
        return redirect('index')
    return render(request, 'main/delete_car.html', {'car': car})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'main/register.html', {'form': form})

def user_login(request):
    next_url = request.GET.get('next', 'index')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.POST.get('next', 'index')
            messages.success(request, "Login successful.")
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    return render(request, 'main/login.html', {'form': form, 'next': next_url})

def user_logout(request):
    logout(request)
    messages.success(request, "Logout successful.")
    return redirect('index')

@login_required
def add_comment(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.car = car
            comment.user = request.user
            comment.save()
            return redirect('car_detail', car_id=car.id)
    else:
        form = CommentForm()
    return render(request, 'main/add_comment.html', {'form': form})
