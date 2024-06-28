from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem, BookedWorkshop
from workshops.models import Workshop
from datetime import datetime
from django.views.generic import TemplateView
from django.views.decorators.http import require_POST
from accounts.models import Profile
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


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
def book_now(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        return redirect('cart')  # Redirect to cart or handle error

    profile, created = Profile.objects.get_or_create(user=request.user)
    for item in cart.items.all():
        BookedWorkshop.objects.create(
            user=request.user,
            workshop=item.workshop,
            date_time=item.date_time,
            quantity=item.quantity
        )
        profile.booked_workshops.add(item.workshop)

    subject = 'Workshop Booking Confirmation'
    context = {
        'user': request.user,
        'items': cart.items.all(),
    }
    html_message = render_to_string('emails/booking_confirmation.html', context)
    plain_message = strip_tags(html_message)

    try:
        send_mail(subject, plain_message, settings.DEFAULT_FROM_EMAIL, ['oceanofnotions@gmail.com'], html_message=html_message)
    except Exception as e:
        print(f"Failed to send email to admin: {e}")

    try:
        send_mail(subject, plain_message, settings.DEFAULT_FROM_EMAIL, [request.user.email], html_message=html_message)
    except Exception as e:
        print(f"Failed to send email to user: {e}")

    cart.items.all().delete()
    return redirect('payment_successful')

@login_required
def payment_success(request):
    # Logic for handling payment success
    return render(request, 'purchase/payment_success.html')

@login_required
def payment_failure(request):
    # Logic for handling payment failure
    return render(request, 'purchase/payment_failure.html')



