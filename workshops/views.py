from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Workshop, WorkshopDateTime  # Workshop model import changed
from .forms import WorkshopBookingForm
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_date, parse_time
from datetime import datetime
from .models import Booking  # Booking model import changed






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
           selected_date = parse_date(form.cleaned_data['date'])
           selected_time = parse_time(form.cleaned_data['time'])
           date_time = datetime.combine(selected_date, selected_time)


           if Booking.objects.filter(workshop=workshop, date_time=date_time).exists():
               return render(request, 'workshops/book_workshop.html', {
                   'form': form,
                   'workshop': workshop,
                   'error_message': 'This time slot is already booked. Please choose another.'
               })


           return redirect('add_to_cart', workshop_id=workshop.id, date_time=date_time.isoformat())


   else:
       form = WorkshopBookingForm(workshop_id=workshop_id)


   return render(request, 'workshops/book_workshop.html', {'form': form, 'workshop': workshop})


