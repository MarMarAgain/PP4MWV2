from django.db import models
from datetime import date

class Workshop(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=50, default='General')
    duration = models.CharField(max_length=50, default='90 minutes')
    date = models.DateField(default=date.today)  # Date field added, default added

    def __str__(self):
        return self.title

class WorkshopDateTime(models.Model):
    workshop = models.ForeignKey(Workshop, related_name='dates_times', on_delete=models.CASCADE)
    date_time = models.DateTimeField()

    def __str__(self):
        return f"{self.workshop} - {self.date_time}"




