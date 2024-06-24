from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from workshops.models import Workshop
from datetime import datetime
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

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import Cart

@login_required
def book_now(request):
    # Retrieve the current user's cart
    cart = Cart.objects.get(user=request.user)

    # Prepare email content
    subject = 'Workshop Booking Confirmation'
    message = f'You have successfully booked the following workshops:\n\n'
    for item in cart.items.all():
        message += f'Workshop: {item.workshop.title}\nDate and Time: {item.date_time}\nPrice: €{item.workshop.price}\nQuantity: {item.quantity}\n\n'

    # Send email to admin
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, ['oceanofnotions@gmail.com'])

    # Send email to user
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [request.user.email])

    # Clear the cart after successful booking
    cart.items.all().delete()

    # Redirect to a success page or another view
    return redirect('payment_successful')  # Adjust this URL name as per your URL configuration


@login_required
def payment_success(request):
    # Logic for handling payment success
    return render(request, 'purchase/payment_success.html')

@login_required
def payment_failure(request):
    # Logic for handling payment failure
    return render(request, 'purchase/payment_failure.html')



