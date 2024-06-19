# purchase/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Payment
from workshops.models import Workshop

@login_required
def initiate_payment(request, workshop_id):
    workshop = get_object_or_404(Workshop, id=workshop_id)

    payment = Payment.objects.create(
        workshop=workshop,
        user=request.user,
        amount=workshop.price,
        status='pending',  # Assuming you start with pending status
    )

    # Simulate success scenario
    payment.status = 'completed'
    payment.save()

    return redirect('payment_success')

@login_required
def cart(request):
    return render(request, 'purchase/cart.html', {})

@login_required
def payment_success(request):
    return render(request, 'purchase/payment_success.html')

@login_required
def payment_failure(request):
    return render(request, 'purchase/payment_failure.html')


