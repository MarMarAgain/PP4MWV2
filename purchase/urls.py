from django.urls import path
from . import views
from .views import add_to_cart, cart


urlpatterns = [
   path('initiate/', views.initiate_payment, name='initiate_payment'),
   path('success/', views.payment_success, name='payment_success'),
   path('failure/', views.payment_failure, name='payment_failure'),
   path('add_to_cart/<int:workshop_id>/', add_to_cart, name='add_to_cart'),
   path('cart/', views.cart, name='cart'),
]
