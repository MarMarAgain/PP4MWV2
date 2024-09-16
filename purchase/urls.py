from django.urls import path
from . import views
from .views import CreateStripeCheckoutSessionView
from .views import stripe_webhook

urlpatterns = [
    path('cart/', views.view_cart, name='cart'),
    path('cart/remove/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    #path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.payment_success, name='success'),
    path('cancel/', views.payment_failure, name='cancel'),
    path('add-to-cart/<int:workshop_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart-total/', views.get_cart_total, name='cart-total'),
    path("create-checkout-session/<int:pk>/", CreateStripeCheckoutSessionView.as_view(),
        name="create-checkout-session",
    ),
    path('webhook/', views.stripe_webhook, name='stripe-webhook'),

]