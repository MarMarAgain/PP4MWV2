from django.db import models
from datetime import date
from django.contrib.auth.models import User  # user model added for booking model

class Workshop(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=50, default='General')
    duration = models.CharField(max_length=50, default='90 minutes')
    date = models.DateField(default=date.today)
    image = models.ImageField(upload_to='workshop_images/', null=True, blank=True) #photo for workshop added

    def __str__(self):
        return self.title

    def get_available_dates_times(self):
        return self.dates_times.filter(bookings__isnull=True)


class WorkshopDateTime(models.Model):
    workshop = models.ForeignKey(Workshop, related_name='dates_times', on_delete=models.CASCADE)
    date_time = models.DateTimeField()

    TIME_CHOICES = [
        ('10am', '10 am'),
        ('11am', '11 am'),
        ('12noon', '12 noon'),
        ('2pm', '2 pm'),
        ('3pm', '3 pm'),
        ('4pm', '4 pm'),
    ]
    time_choice = models.CharField(max_length=20, choices=TIME_CHOICES, default='10am')

    def __str__(self):
        return f"{self.workshop} - {self.date_time}"


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    date_time = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} booked {self.workshop.title} at {self.date_time}"


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.workshop.title} for {self.user.username}"
