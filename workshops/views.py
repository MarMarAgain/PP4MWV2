from django.shortcuts import render, get_object_or_404, redirect
from .models import Workshop, WorkshopDateTime, Booking
from django.contrib.auth.decorators import login_required
from django import forms
from .forms import WorkshopBookingForm


def workshop_list(request):
    # Prefetch related dates and times to optimize database queries
    workshops = Workshop.objects.prefetch_related('events').all()
    return render(request, 'workshops/workshop_list.html', {'workshops': workshops})


def workshop_detail(request, workshop_id):
    workshop = get_object_or_404(Workshop, pk=workshop_id)
    # Fetch related WorkshopDateTime instances
    workshop_dates_times = workshop.events.all()
    return render(request, 'workshops/workshop_detail.html', {
        'workshop': workshop,
        'workshop_dates_times': workshop_dates_times
    })


@login_required
def book_workshop(request, workshop_id):
    workshop = get_object_or_404(Workshop, pk=workshop_id)
    workshop_dates_times = workshop.events.all()

    if request.method == 'POST':
        form = WorkshopBookingForm(request.POST, workshop_id=workshop_id)
        if form.is_valid():
            selected_event = form.cleaned_data['event']

            if Booking.objects.filter(workshop=workshop, date_time=selected_event.date_time).exists():
                return render(request, 'workshops/workshop_detail.html', {
                    'form': form,
                    'workshop': workshop,
                    'workshop_dates_times': workshop_dates_times,
                    'error_message': 'This time slot is already booked. Please choose another.'
                })

            Booking.objects.create(
                user=request.user,
                workshop=workshop,
                date_time=selected_event.date_time  # Save the date_time correctly
            )
            return redirect('cart')  # Adjust this redirect to your actual cart view URL

    else:
        form = WorkshopBookingForm(workshop_id=workshop_id)

    return render(request, 'workshops/workshop_detail.html', {
        'form': form,
        'workshop': workshop,
        'workshop_dates_times': workshop_dates_times
    })
