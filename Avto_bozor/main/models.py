from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Brand(models.Model):
    name = models.CharField(max_length=255)
    brand_logo = models.ImageField(upload_to='brand_image/', null=True, blank=True)

    def __str__(self):
        return self.name

class Car(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
    model_name = models.CharField(max_length=100)
    year = models.IntegerField()
    color = models.CharField(max_length=50)
    views = models.IntegerField(default=0)
    scor = models.CharField(max_length=100, null=True, blank=True, verbose_name='boshqaruvi')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    body = models.CharField(max_length=100, null=True, blank=True, verbose_name='kozovi')
    city = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=30, null=True, blank=True)
    engine_volume = models.CharField(max_length=100, null=True, blank=True, verbose_name='divigatel hajmi, l')
    position = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='car_images/')
    kilometers = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.brand} {self.model_name}'

class Comment(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
