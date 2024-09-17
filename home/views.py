from django.shortcuts import render

def index(request):

    return render(request, 'home.html')

def faq_view(request):

    return render(request, 'FAQ.html')
