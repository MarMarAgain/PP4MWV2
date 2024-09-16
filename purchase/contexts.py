from decimal import Decimal
from .models import Cart, CartItem

def cart_total_processor(request):
    bag_items = []
    total = Decimal('0.00')

    # Handle authenticated user
    if request.user.is_authenticated:
        try:
            # Retrieve the cart for the logged-in user
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            # If no cart exists, return an empty cart context
            cart = None
    else:
        # Handle anonymous user cart via session
        cart = None
        session_cart = request.session.get('cart', {})
        for item_id, item_data in session_cart.items():
            # Assuming item_data has workshop details and quantity
            workshop = item_data['workshop']  # Mock workshop data or fetch it from the database
            price = Decimal(item_data['price'])
            quantity = item_data['quantity']
            total += price * quantity

            bag_items.append({
                'workshop': workshop,
                'price': price,
                'quantity': quantity,
            })

    # If cart exists, calculate the total and items for logged-in user
    if cart:
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

