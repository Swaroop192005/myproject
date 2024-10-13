from django.contrib import admin
from .models import UserProfile, Guest, Room, Booking

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Guest)
admin.site.register(Room)  # Keep this registration
admin.site.register(Booking)
