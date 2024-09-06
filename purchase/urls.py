from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.view_cart, name='cart'),
    path('cart/remove/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('payment-successful/', views.payment_success, name='payment_successful'),
    path('payment-failure/', views.payment_failure, name='payment_failure'),
    path('add-to-cart/<int:workshop_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/total/', views.get_cart_total, name='get_cart_total'),
]
