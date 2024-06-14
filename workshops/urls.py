from django.urls import path
from .views import workshop_list, workshop_detail, book_workshop, add_to_cart, cart_view

urlpatterns = [
    path('', workshop_list, name='workshop_list'),
    path('workshop/<int:workshop_id>/', workshop_detail, name='workshop_detail'),
    path('workshop/<int:workshop_id>/book/', book_workshop, name='book_workshop'),
    path('workshop/<int:workshop_id>/add_to_cart/',add_to_cart, name='add_to_cart'),
    path('cart/', cart_view, name='cart_view'),

]
