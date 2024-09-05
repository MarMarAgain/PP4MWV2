from django.db import models
from datetime import date
from django.contrib.auth.models import User


class Workshop(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)  # Larger max_digits than Product
    category = models.CharField(max_length=50, default='General')
    duration = models.CharField(max_length=50, default='90 minutes')
    image = models.ImageField(upload_to='workshop_images/', null=True, blank=True)
    is_canceled = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class WorkshopDateTime(models.Model):  # Equivalent to CalendarEvent
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, related_name='events')
    date_time = models.DateTimeField()  # Renamed from date_time for consistency
    location = models.CharField(max_length=255, default ="school")  # Added location field

def __str__(self):
    return f"Event for {self.workshop.title} on {self.date_time}"



class Booking(models.Model):  # Booking is already quite similar
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    date_time = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} booked {self.workshop.title} at {self.event.date_time}"

