from django.contrib import admin
from django.urls import path, include  # Import include to reference the app's URLs

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('hotel.urls')),  # Include the hotel app URLs
]
