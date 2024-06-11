from django.urls import path
from .views import workshop_list

app_name = 'workshops'

urlpatterns = [
    path('', workshop_list, name='workshop_list'),
]
