import stripe
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from .contexts import cart_total_processor
from workshops.models import Workshop, Booking
from purchase.models import CartItem
from django.contrib.auth.models import User
from datetime import datetime
from .stripe_func import create_customer, attach_payment_method
import json
from django.views import View
from django.views.generic import TemplateView
from stripe import webhook
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

# Stripe API Key
stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def get_cart_total(request):
    cart = Cart.objects.filter(user=request.user).first()  # Assuming one cart per user
    if cart:
        total = sum(
            item.workshop.price * item.quantity for item in cart.items.all())  # items is a related_name for CartItems
    else:
        total = 0.0

    return JsonResponse({'total': total})


# Add to Cart
@login_required
def add_to_cart(request, workshop_id):
    if request.method == 'POST':
        workshop = get_object_or_404(Workshop, pk=workshop_id)
        date_time_str = request.POST.get('date_time')

        try:
            date_time = datetime.fromisoformat(date_time_str)
        except ValueError:
            return JsonResponse({'message': 'Invalid date format.'}, status=400)

        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            workshop=workshop,
            date_time=date_time,
            defaults={'quantity': 1}
        )

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Workshop added to cart successfully!'})

        return redirect('cart')

    return JsonResponse({'message': 'Invalid request method.'}, status=400)


# View Cart
@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    if not cart.items.exists():
        return render(request, 'purchase/cart.html', {
            'cart': cart,
            'total': 0,
            'error': 'Your cart is empty. Add items to proceed.'
        })

    # Calculate the total price in cents
    total_cents = sum(item.workshop.price * item.quantity for item in cart.items.all()) * 100

    try:
        payment_intent = stripe.PaymentIntent.create(
            amount=int(total_cents),  # Amount in cents
            currency='eur',
            payment_method_types=['card'],
        )
    except stripe.error.StripeError as e:
        return render(request, 'purchase/cart.html', {
            'cart': cart,
            'total': total_cents / 100,  # Convert to euros for display
            'error': str(e)
        })

    return render(request, 'purchase/cart.html', {
        'cart': cart,
        'total': total_cents / 100  # Total in euros for display
    })


class CreateStripeCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        # Get the user's cart
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)

        line_items = []

        # Loop through each cart item and add to line_items
        for cart_item in cart_items:
            line_items.append({
                'price_data': {
                    'currency': 'eur',
                    'product_data': {
                        'name': cart_item.workshop.title,
                        'description': cart_item.workshop.description,
                        'images': [f"{settings.BACKEND_DOMAIN}{cart_item.workshop.image.url}"],
                    },
                    'unit_amount': int(cart_item.workshop.price * 100),  # Price in cents
                },
                'quantity': cart_item.quantity,
            })

        # Create a Stripe Checkout session
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=request.build_absolute_uri(reverse('success')),
                cancel_url=request.build_absolute_uri(reverse('cancel')),
                metadata={
                    'user_id': request.user.id,  # Add the user's ID to the metadata
                    'workshop_ids': ",".join([str(item.workshop.id) for item in cart_items])  # Include workshop IDs
                }
            )

            # Redirect to Stripe's checkout page
            return redirect(checkout_session.url, code=303)

        except stripe.error.StripeError as e:
            # Handle Stripe API errors
            return JsonResponse({'error': str(e)}, status=400)


# Remove Cart Item
@login_required
def remove_cart_item(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id)
        cart_item.delete()

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Workshop added to cart successfully!'})
        return redirect('view_cart')

    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)


@login_required
def payment_success(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart.items.all().delete()  # Remove all items from the cart
    except Cart.DoesNotExist:
        pass  # If no cart exists, do nothing
    return render(request, 'purchase/payment_success.html')


@login_required
def payment_failure(request):
    return render(request, 'purchase/payment_failure.html')


# stripe webhook
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        # Verify the webhook signature
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle successful payment event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Check if payment was completed successfully
        if session.mode == 'payment' and session.payment_status == 'paid':
            try:
                # Extract user and workshop information from session metadata
                user_id = session['metadata']['user_id']
                workshop_ids = session['metadata']['workshop_ids'].split(',')
                user = User.objects.get(id=user_id)
            except (User.DoesNotExist, KeyError):
                # Handle missing user or metadata
                return HttpResponse(status=404)

            # Process each workshop and create a booking
            for workshop_id in workshop_ids:
                try:
                    # Fetch the workshop instance
                    workshop = Workshop.objects.get(id=workshop_id)

                    # Create a new booking
                    Booking.objects.create(
                        user=user,
                        workshop=workshop,
                        date_time=timezone.now(),  # Booking time is now
                        total_price=workshop.price,  # Use the workshop price
                        stripe_checkout_id=session['id']  # Store Stripe session ID
                    )
                except Workshop.DoesNotExist:
                    # Handle the case where a workshop is not found
                    continue  # Skip this workshop if not found

            # Return a 200 response when bookings are successfully created
            return HttpResponse(status=200)

    # Return 400 if the event type is not handled
    return HttpResponse(status=400)



