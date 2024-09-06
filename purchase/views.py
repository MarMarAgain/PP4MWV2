import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from django.views.decorators.http import require_POST
from workshops.models import Workshop
from django.utils.dateparse import parse_datetime
from datetime import datetime
from .stripe_func import create_customer, attach_payment_method
import json

@login_required
def add_to_cart(request, workshop_id):
    if request.method == 'POST':
        workshop = get_object_or_404(Workshop, pk=workshop_id)
        date_time_str = request.POST.get('date_time')
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

    return JsonResponse({'message': 'Invalid request method.'}, status=400)


@login_required
def view_cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=request.user)

    return render(request, 'purchase/cart.html', {'cart': cart})

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def create_checkout_session(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        payment_method_id = data.get('payment_method_id')

        # Create a Stripe customer
        customer = create_customer(email)

        # Attach the payment method to the customer
        attach_payment_method(customer.id, payment_method_id)

        # Create a payment intent or session and return the client secret or session ID
        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=1000,  # Example amount in cents
                currency='usd',
                customer=customer.id,
                payment_method=payment_method_id,
                off_session=True,
                confirm=True,
            )
            return JsonResponse({'client_secret': payment_intent.client_secret})
        except stripe.error.StripeError as e:
            return JsonResponse({'error': str(e)}, status=400)

    return render(request, 'purchase/cart.html')

@login_required
def remove_cart_item(request, item_id):
    if request.method == 'POST':
        print(f"Request to remove item with ID: {item_id}")  # Log to terminal for debugging- can remove later
        cart_item = get_object_or_404(CartItem, id=item_id)
        cart_item.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)



@login_required
def payment_success(request):
    return render(request, 'purchase/payment_success.html')


@login_required
def payment_failure(request):
    return render(request, 'purchase/payment_failure.html')







