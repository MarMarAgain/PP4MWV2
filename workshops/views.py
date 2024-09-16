from django.shortcuts import render, get_object_or_404, redirect
from .models import Workshop, WorkshopDateTime, Booking
from django.contrib.auth.decorators import login_required
from django import forms

# Form for booking a workshop
class WorkshopBookingForm(forms.Form):
    date_time = forms.ModelChoiceField(queryset=WorkshopDateTime.objects.none())

    def __init__(self, *args, **kwargs):
        workshop_id = kwargs.pop('workshop_id', None)
        super().__init__(*args, **kwargs)
        if workshop_id:
            self.fields['event'].queryset = WorkshopDateTime.objects.filter(workshop_id=workshop_id)

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
    # Fetch related WorkshopDateTime instances
    workshop_dates_times = workshop.events.all()

    if request.method == 'POST':
        form = WorkshopBookingForm(request.POST, workshop_id=workshop_id)
        if form.is_valid():
            selected_event = form.cleaned_data['event']
            # Check if the selected event is already booked
            if Booking.objects.filter(workshop=workshop, date_time=selected_event.date_time).exists():
                return render(request, 'workshops/workshop_detail.html', {
                    'form': form,
                    'workshop': workshop,
                    'workshop_dates_times': workshop_dates_times,
                    'error_message': 'This time slot is already booked. Please choose another.'
                })

            # Create and save the booking
            Booking.objects.create(
                user=request.user,
                workshop=workshop,
                event=selected_event
            )
            return redirect('cart_view')  # Adjust to your actual redirect URL

    else:
        form = WorkshopBookingForm(workshop_id=workshop_id)  # Initialize form with available events

    return render(request, 'workshops/workshop_detail.html', {
        'form': form,
        'workshop': workshop,
        'workshop_dates_times': workshop_dates_times
    })

