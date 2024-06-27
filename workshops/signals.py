from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from accounts.models import Profile


@receiver(m2m_changed, sender=Profile.booked_workshops.through)
def workshop_booking_handler(sender, instance, action, **kwargs):
    if action == "post_add":
        workshop = instance.booked_workshops.last()
        subject = "Workshop Booking Confirmation"
        html_message = render_to_string('emails/booking_confirmation.html', {'workshop': workshop, 'user': instance.user})
        plain_message = strip_tags(html_message)
        to_email = instance.user.email
        admin_email = 'oceanofnotions@gmail.com'
        send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [to_email, admin_email], html_message=html_message)

    elif action == "post_remove":
        workshop = kwargs['pk_set']
        subject = "Workshop Cancellation Confirmation"
        html_message = render_to_string('emails/cancellation_confirmation.html', {'workshop': workshop, 'user': instance.user})
        plain_message = strip_tags(html_message)
        to_email = instance.user.email
        admin_email = 'oceanofnotions@gmail.com'
        send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [to_email, admin_email], html_message=html_message)
