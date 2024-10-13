from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Room, Booking, Rating
from datetime import datetime

# views.py


from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('dashboard')  # Replace 'dashboard' with the name of your redirect page
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})




from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm



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

from django.shortcuts import render
from .models import Guest, Booking, Room

from django.shortcuts import render
from hotel.models import Booking

from django.shortcuts import render
from hotel.models import Booking

# Add this function to your views.py file
from django.shortcuts import render
from hotel.models import Booking

from django.shortcuts import render
from hotel.models import Booking
from django.utils.dateparse import parse_date

def dashboard(request):
    # Fetch all bookings
    bookings = Booking.objects.select_related('guest__user').all()

    # Check if there's a search query for guest name
    query = request.GET.get('q')
    if query:
        bookings = bookings.filter(guest__user__name__icontains=query)

    # Check if there's a search query for check-out date
    checkout_date = request.GET.get('checkout_date')
    if checkout_date:
        # Parse the checkout_date to a Python date object
        parsed_date = parse_date(checkout_date)
        if parsed_date:
            bookings = bookings.filter(check_out_date=parsed_date)

    return render(request, 'dashboard.html', {
        'bookings': bookings,
        'query': query,
        'checkout_date': checkout_date,
    })




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
