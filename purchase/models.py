from django.db import models
from payments.models import BasePayment
from payments import PurchasedItem
from django.utils import timezone #added for timestamp in payment class

class Payment(BasePayment):
    workshop = models.ForeignKey('workshops.Workshop', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now) #changed due to migration issues
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed')])

    class Meta:
        app_label = 'purchase' #added to specify app-label

    def __str__(self):
        return f"{self.user.username} - {self.workshop.title} - {self.amount}"

    def get_failure_url(self):
        return 'payment_failure'

    def get_success_url(self):
        return 'payment_success'

    def get_purchased_items(self):
        yield PurchasedItem(
            name=self.workshop.title,
            sku=str(self.workshop.id),
            quantity=1,
            price=self.amount,
            currency='EUR', #changed currency
        )

