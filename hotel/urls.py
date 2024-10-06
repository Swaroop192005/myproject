# hotel/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.dashboard, name='dashboard'),  # Ensure this is below login path
    path('available-rooms/', views.available_rooms, name='available_rooms'),
    path('book-room/', views.book_room, name='book_room'),
    path('leave-rating/', views.leave_rating, name='leave_rating'),
]
