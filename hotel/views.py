from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Room, Booking, Rating
from datetime import datetime

# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Authenticate and log the user in
            auth_login(request, form.get_user())
            return redirect('dashboard')  # Redirect to the dashboard or another page after login
    else:
        form = AuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})

def available_rooms(request):
    rooms = Room.objects.filter(status='Available')  # Corrected field name
    return render(request, 'rooms_available.html', {'rooms': rooms})

def book_room(request):
    if request.method == 'POST':
        room_id = request.POST['room']
        checkin = datetime.strptime(request.POST['checkin'], '%Y-%m-%d').date()  # Convert string to date
        checkout = datetime.strptime(request.POST['checkout'], '%Y-%m-%d').date()  # Convert string to date
        
        # Assuming user is logged in, use request.user
        guest = request.user.guest

        room = get_object_or_404(Room, id=room_id)  # Use get_object_or_404 for safety
        total_amount = room.price * (checkout - checkin).days  # Use correct field names

        # Create Booking
        Booking.objects.create(guest=guest, room=room, check_in_date=checkin, check_out_date=checkout, total_amount=total_amount)

        # Change room status to Occupied
        room.status = 'Occupied'
        room.save()

        return redirect('dashboard')  # Redirect to dashboard or booking success page

    rooms = Room.objects.filter(status='Available')
    return render(request, 'book_room.html', {'rooms': rooms})

def dashboard(request):
    bookings = Booking.objects.all()
    return render(request, 'dashboard.html', {'bookings': bookings})

def leave_rating(request):
    if request.method == 'POST':
        booking_id = request.POST['booking']
        rating = request.POST['rating']
        review = request.POST['review']
        
        booking = get_object_or_404(Booking, id=booking_id, guest__user=request.user)  # Ensure it's the user's booking
        Rating.objects.create(booking=booking, rating=rating, review=review)

        return HttpResponse("Rating submitted successfully!")
    
    # Fetch bookings for the logged-in user
    bookings = Booking.objects.filter(guest__user=request.user)
    
    return render(request, 'leave_rating.html', {'bookings': bookings})
# views.py
