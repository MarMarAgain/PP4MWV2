# purchase/models.py

from django.db import models
from django.utils import timezone
from workshops.models import Workshop
from django.contrib.auth.models import User

class Payment(models.Model):
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed')])

    class Meta:
        app_label = 'purchase'

    def __str__(self):
        return f"{self.user.username} - {self.workshop.title} - {self.amount}"

    def get_failure_url(self):
        return 'payment_failure'

    def get_success_url(self):
        return 'payment_success'
