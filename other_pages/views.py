from django.shortcuts import render

def landing_page(request):
    return render(request, 'Other/landing_page.html')
