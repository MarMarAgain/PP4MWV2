from decimal import Decimal
from django.shortcuts import get_object_or_404
from workshops.models import Workshop, WorkshopDateTime

def bag_contents(request):
    bag_items = []
    total = Decimal('0.00')

    # Assume the bag structure is {product_id: event_id}
    bag = request.session.get('bag', {})

    for product_id, event_id in bag.items():
        product = get_object_or_404(Workshop, pk=product_id)
        event = get_object_or_404(WorkshopDateTime, pk=event_id)
        price = Decimal(product.price)
        # Add quantity to the total amount calculation
        quantity = bag.get('quantity', 1)  # Default to 1 if quantity not specified
        total += price * quantity

        bag_items.append({
            'product': product,
            'event': event,
            'price': price,
            'quantity': quantity,  # Include quantity in the context
        })

    context = {
        'bag_items': bag_items,
        'total': total,
    }

    return context
