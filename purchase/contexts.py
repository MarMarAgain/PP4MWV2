# purchase/contexts.py
from decimal import Decimal
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem

def cart_total_processor(request):
    bag_items = []
    total = Decimal('0.00')

    try:
        # Retrieve the cart for the logged-in user
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        # If no cart exists, initialize an empty cart
        cart = Cart()

    # Iterate through items in the cart
    for item in cart.items.all():
        workshop = item.workshop
        price = Decimal(workshop.price)
        quantity = item.quantity
        total += price * quantity

        bag_items.append({
            'workshop': workshop,
            'price': price,
            'quantity': quantity,
        })

    context = {
        'bag_items': bag_items,
        'total': total,
    }

    return context

