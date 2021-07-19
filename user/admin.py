from django.contrib import admin
from .models import *
from plant.models import *

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'password', 'profile_picture', 'user_address')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'line1', 'line2', 'city', 'state', 'zip_code', 'user')

@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'price', 'quantity', 'picture')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'amounts', 'order_sum')

