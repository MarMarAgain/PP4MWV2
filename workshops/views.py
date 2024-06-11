from django.shortcuts import render
from .models import Workshop

def workshop_list(request):
    workshops = Workshop.objects.all()
    return render(request, 'workshops/workshop_list.html', {'workshops': workshops})

