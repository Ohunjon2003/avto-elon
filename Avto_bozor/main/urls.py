from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('car/<int:car_id>/', views.car_detail, name='car_detail'),
    path('brands/<int:brand_id>/', views.brand_cars, name='brand_cars'),
    path('create/', views.create_car, name='create_car'),
    path('update/<int:car_id>/', views.update_car, name='update_car'),
    path('delete/<int:car_id>/', views.delete_car, name='delete_car'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),


]
