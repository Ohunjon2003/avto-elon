from django.contrib import admin
from .models import Comment, Car, Brand


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model_name', 'year', 'color', 'price', 'created_at')
    list_filter = ('brand', 'year', 'color')
    search_fields = ('brand__name', 'model_name', 'color', 'city')


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Comment)
