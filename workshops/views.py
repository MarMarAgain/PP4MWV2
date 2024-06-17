# views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Workshop, WorkshopDateTime, Booking, CartItem
from .forms import WorkshopBookingForm
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_date, parse_time
from datetime import datetime

def workshop_list(request):
    workshops = Workshop.objects.all()
    return render(request, 'workshops/workshop_list.html', {'workshops': workshops})

def workshop_detail(request, workshop_id):
    workshop = get_object_or_404(Workshop, pk=workshop_id)
    workshops = Workshop.objects.all()  # Fetch all workshops
    return render(request, 'workshops/workshop_detail.html', {'workshop': workshop, 'workshops': workshops})

@login_required
def book_workshop(request, workshop_id):
    workshop = get_object_or_404(Workshop, pk=workshop_id)

    if request.method == 'POST':
        form = WorkshopBookingForm(request.POST, workshop_id=workshop_id)
        if form.is_valid():
            selected_date = parse_date(form.cleaned_data['date'])
            selected_time = parse_time(form.cleaned_data['time'])
            date_time = datetime.combine(selected_date, selected_time)

            # Check if the time slot is already booked
            if Booking.objects.filter(workshop=workshop, date_time=date_time).exists():
                return render(request, 'workshops/book_workshop.html', {
                    'form': form,
                    'workshop': workshop,
                    'error_message': 'This time slot is already booked. Please choose another.'
                })

            # Redirect to the add_to_cart view to handle adding the item to the cart
            return redirect('add_to_cart', workshop_id=workshop.id, date_time=date_time.isoformat())

    else:
        form = WorkshopBookingForm(workshop_id=workshop_id)

    return render(request, 'workshops/book_workshop.html', {'form': form, 'workshop': workshop})


def bookings(request):
    return render(request, 'workshops/bookings.html')

@login_required
def add_to_cart(request, workshop_id, date_time):
    workshop = get_object_or_404(Workshop, pk=workshop_id)
    date_time = datetime.fromisoformat(date_time)

    # Add the workshop to the user's cart
    CartItem.objects.create(user=request.user, workshop=workshop, date_time=date_time, quantity=1)

    return redirect('cart_view')

@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    return render(request, 'workshops/cart.html', {'cart_items': cart_items})


