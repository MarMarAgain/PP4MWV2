from django.shortcuts import render, get_object_or_404
from .models import Payment
from workshops.models import Workshop
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

class PaymentView(TemplateView):
    template_name = 'payments/payment_form.html'

@login_required
def initiate_payment(request, workshop_id):
    workshop = get_object_or_404(Workshop, id=workshop_id)
    # Build logic to initiate payment, e.g., interacting with a payment gateway
    return render(request, 'payments/payment_form.html', {'workshop': workshop})

@login_required
def payment_success(request):
    # Build logic for handling successful payment
    return render(request, 'payments/payment_success.html')

@login_required
def payment_failure(request):
    # Build logic for handling failed payment
    return render(request, 'payments/payment_failure.html')
