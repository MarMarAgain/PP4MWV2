from django.db import models

class Workshop(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=50, default='General')
    duration = models.CharField(max_length=50, default='90 minutes')
# may have to develop duration and catagory for admin panel
    def __str__(self):
        return self.title



