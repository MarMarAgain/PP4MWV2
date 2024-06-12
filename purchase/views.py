from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .models import Payment
from workshops.models import Workshop
from payments import get_payment_model, RedirectNeeded

class PaymentView(TemplateView):
    template_name = 'purchase/payment_form.html'

@login_required
def initiate_payment(request, workshop_id):
    workshop = get_object_or_404(Workshop, id=workshop_id)
    Payment = get_payment_model()

    payment = Payment.objects.create(
        variant='default',  # check this  with settings
        user=request.user,
        workshop=workshop,
        amount=workshop.price,
        currency='EUR',
        description=f'Payment for {workshop.title}',
    )

    try:
        payment.change_status('waiting')
        return redirect(payment.get_process_url())
    except RedirectNeeded as redirect_to:
        return redirect(str(redirect_to))

@login_required
def payment_success(request):
    # Implement logic to handle successful payment, e.g., updating workshop booking status
    return render(request, 'purchase/payment_success.html')

@login_required
def payment_failure(request):
    # Implement logic to handle failed payment
    return render(request, 'purchase/payment_failure.html')
