from django.db import models
from django.contrib.auth.models import User
from workshops.models import Workshop

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)



class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    date_time = models.DateTimeField(null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.workshop.title} for {self.cart.user.username}"

class SimulatedPayment(models.Model):  # Changed to simulated_payment as I don't have access to stripe dashboard
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')])

    def __str__(self):
        return f"{self.user.username} - ${self.amount} - {self.get_status_display()}"

