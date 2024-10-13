from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import UserProfile, Guest, Room, Booking

admin.site.register(UserProfile)
admin.site.register(Guest)
admin.site.register(Room)
admin.site.register(Booking)
