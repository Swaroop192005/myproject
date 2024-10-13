from django.db import models
from django.contrib.auth.models import User  # Use Django's built-in User model

class UserProfile(models.Model):
    USER_ROLE_CHOICES = [
        ('Hotel', 'Hotel'),
        ('Customer', 'Customer'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=USER_ROLE_CHOICES)
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

class Guest(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    id_proof = models.CharField(max_length=50)

from django.db import models

class Room(models.Model):
    room_type = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_rooms = models.PositiveIntegerField(default=100)  # Total number of rooms
    available_rooms = models.PositiveIntegerField(default=100)  # Currently available rooms

    def __str__(self):
        return f"{self.room_type} - Price: {self.price} - Available: {self.available_rooms}"


class Booking(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    booking_status = models.CharField(max_length=20, default='Confirmed')

    class Meta:  # Corrected indentation
        constraints = [
            models.CheckConstraint(
                check=models.Q(check_out_date__gt=models.F('check_in_date')),
                name='check_out_after_check_in'
            )
        ]

    def __str__(self):
        return f"Booking for {self.guest.user.name} in {self.room.room_type}"

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('Credit Card', 'Credit Card'),
        ('Cash', 'Cash'),
        ('Online', 'Online'),
    ]
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_date = models.DateTimeField(auto_now_add=True)

class Rating(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.TextField()

    def save(self, *args, **kwargs):
        # Validate that rating is between 1 and 5
        if not (1 <= self.rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
        super().save(*args, **kwargs)  # Call the parent class's save method

    def __str__(self):
        return f"Rating for Booking ID: {self.booking.id} - Rating: {self.rating}"

class Employee(models.Model):
    ROLE_CHOICES = [  # Added ROLE_CHOICES definition
        ('Manager', 'Manager'),
        ('Housekeeping', 'Housekeeping'),
        ('Receptionist', 'Receptionist'),
        ('Maintenance', 'Maintenance'),
    ]
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    shift = models.CharField(max_length=15)
    hire_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - {self.role}"
