from django.db import models

class Payment(models.Model):
    workshop = models.ForeignKey('workshops.Workshop', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed')])

    def __str__(self):
        return f"{self.user.username} - {self.workshop.title} - {self.amount}"
