from django.urls import path
from . import views
from .views import add_to_cart


urlpatterns = [
   path('book-now/', views.book_now, name='book_now'),
   path('payment-successful/', views.payment_success, name='payment_successful'),
   path('failure/', views.payment_failure, name='payment_failure'),
   path('add_to_cart/<int:workshop_id>/', add_to_cart, name='add_to_cart'),
   path('cart/', views.cart, name='cart'),
   path('remove/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
]
