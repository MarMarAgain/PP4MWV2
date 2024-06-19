from django.urls import path
from . import views


urlpatterns = [
   path('', views.workshop_list, name='workshop_list'),
   path('<int:workshop_id>/', views.workshop_detail, name='workshop_detail'),
   path('<int:workshop_id>/book/', views.book_workshop, name='book_workshop'),
]
