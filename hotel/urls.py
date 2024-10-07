# hotel/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views



urlpatterns = [
    path('', views.login_view, name='login'),  # Using your custom login view
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),  # Corrected the missing quote
    path('available-rooms/', views.available_rooms, name='available_rooms'),
    path('book-room/', views.book_room, name='book_room'),
    path('leave-rating/', views.leave_rating, name='leave_rating'),
]
