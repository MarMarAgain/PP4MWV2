from django.urls import path
from .views import PaymentView, initiate_payment, payment_success, payment_failure

urlpatterns = [
    path('form/', PaymentView.as_view(), name='payment_form'),
    path('initiate/<int:workshop_id>/', initiate_payment, name='initiate_payment'),
    path('success/', payment_success, name='payment_success'),
    path('failure/', payment_failure, name='payment_failure'),
]
