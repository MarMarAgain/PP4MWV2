from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from workshops.models import Workshop
from datetime import datetime
from .models import SimulatedPayment
from django.views.generic import TemplateView
from django.views.decorators.http import require_POST


@login_required
def add_to_cart(request, workshop_id):
    workshop = get_object_or_404(Workshop, pk=workshop_id)
    date_time_str = request.GET.get('date_time')
    date_time = datetime.fromisoformat(date_time_str)

    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        workshop=workshop,
        date_time=date_time,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    if request.is_ajax():
        return JsonResponse({'message': 'Workshop added to cart successfully!'})

    return redirect('cart')



@login_required
class PaymentView(TemplateView):
    template_name = 'purchase/payment_form.html'


@require_POST
def remove_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return JsonResponse({'success': True})

@login_required
def cart(request):
    try:
        cart = request.user.cart
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=request.user)

    return render(request, 'purchase/cart.html', {'cart': cart})

@login_required
def initiate_payment(request):
    workshop_id = request.POST.get('workshop_id')
    amount = request.POST.get('amount')
    user = request.user

    # Simulate creating a payment record
    SimulatedPayment.objects.create(
        user=user,
        amount=amount,
        status='completed'  # Simulate a successful payment for demo purposes
    )

    return redirect('payment_success')  # Redirect to success page

@login_required
def payment_success(request):
    # Logic for handling payment success
    return render(request, 'purchase/payment_success.html')

@login_required
def payment_failure(request):
    # Logic for handling payment failure
    return render(request, 'purchase/payment_failure.html')



