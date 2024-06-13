from django.shortcuts import render, get_object_or_404, redirect
from .models import Workshop, WorkshopDateTime, Booking, CartItem
from .forms import WorkshopBookingForm
from django.contrib.auth.decorators import login_required

def workshop_list(request):
    workshops = Workshop.objects.all()
    return render(request, 'workshops/workshop_list.html', {'workshops': workshops})

def workshop_detail(request, workshop_id):
    workshop = get_object_or_404(Workshop, pk=workshop_id)
    return render(request, 'workshops/workshop_detail.html', {'workshop': workshop})

@login_required
def book_workshop(request, workshop_id):
    workshop = get_object_or_404(Workshop, pk=workshop_id)

    if request.method == 'POST':
        form = WorkshopBookingForm(request.POST, workshop_id=workshop_id)
        if form.is_valid():
            date_time_id = form.cleaned_data['date_time']
            date_time = WorkshopDateTime.objects.get(id=date_time_id)

            # Check if the time slot is already booked
            if Booking.objects.filter(workshop=workshop, date_time=date_time.date_time).exists():
                return render(request, 'workshops/book_workshop.html', {
                    'form': form,
                    'workshop': workshop,
                    'error_message': 'This time slot is already booked. Please choose another.'
                })

            # Redirect to the add_to_cart view to handle adding the item to the cart
            return redirect('add_to_cart', workshop_id=workshop.id, date_time_id=date_time.id)

    else:
        form = WorkshopBookingForm(workshop_id=workshop_id)

    return render(request, 'workshops/book_workshop.html', {'form': form, 'workshop': workshop})

@login_required
def add_to_cart(request, workshop_id, date_time_id):
    workshop = get_object_or_404(Workshop, pk=workshop_id)
    date_time = get_object_or_404(WorkshopDateTime, pk=date_time_id)

    # Add the workshop to the user's cart
    CartItem.objects.create(user=request.user, workshop=workshop, date_time=date_time.date_time, quantity=1)

    return redirect('cart_view')

@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    return render(request, 'workshops/cart.html', {'cart_items': cart_items})



