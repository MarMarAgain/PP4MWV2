import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from .contexts import cart_total_processor
from workshops.models import Workshop, Booking
from datetime import datetime
from django.utils import timezone
from .stripe_func import create_customer, attach_payment_method
import json
from django.contrib.auth.models import User
from django.http import HttpResponse



@login_required
def get_cart_total(request):
    context = cart_total_processor(request)
    return JsonResponse({'total': str(context['total'])})


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

    # Calculate the total price in cents (Stripe expects the amount in cents)
    total = sum(item.workshop.price * item.quantity for item in cart.items.all()) * 100  # multiply by 100 for cents

    # Create a PaymentIntent on page load
    try:
        payment_intent = stripe.PaymentIntent.create(
            amount=int(total),  # amount in cents
            currency='eur',
            payment_method_types=['card'],
        )
    except stripe.error.StripeError as e:
        return render(request, 'purchase/cart.html', {
            'cart': cart,
            'total': total / 100,  # total in euros for display
            'error': str(e)  # pass error to the template
        })

    # Pass client_secret to the template
    return render(request, 'purchase/cart.html', {
        'cart': cart,
        'total': total / 100,  # total in euros for display
        'client_secret': payment_intent.client_secret  # pass the client_secret to the template
    })


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
                amount=1000,  # Amount in cents
                currency='eur',
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

#stripe webhook
def stripe_webhook(request):
    payload=request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret=settings.STRIPE_WEBHOOK_SECRET

    try:
        event=stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.StripeError:
        return HttpResponse(status=400)

    if event['type']=='checkout.session.completed':
        session = event['data']['object']

        if session.mode =='payment' and session.payment_status == 'paid':
            try:
                user_id = session['metadata']['user_id']
                workshop_ids = session['metadata']['workshop_ids'].split(',')
                user = User.objects.get(id=user_id)
            except (User.DoesNotExist, KeyError):
                return HttpResponse(status=400)

            for workshop_id in workshop_ids:
                try:
                    workshop = Workshop.objects.get(id=workshop_id)

                    Booking.objects.create(
                        user=user,
                        workshop=workshop,
                        date_time=timezone.now(),
                        total_price=workshop.price,
                        stripe_checkout_id=session['id']
                    )

                except Workshop.DoesNotExist:
                    continue

            return HttpResponse(status=200)

    return HttpResponse(status=400)





