from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from accounts.forms import CustomUserCreationForm, ProfileForm
from django.contrib import messages
from django.core.mail import send_mail
from workshops.models import Workshop, Review, Booking
from workshops.forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from purchase.models import BookedWorkshop
from accounts.models import Profile


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')  # Redirect to profile page after successful signup
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        user = form.save()  # This will save both User and Profile due to form's save method
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=user.username, password=raw_password)
        if user is not None:
            login(self.request, user)
            messages.success(self.request, 'Account created successfully!')
            return redirect(self.success_url)
        else:
            messages.error(self.request, 'Failed to authenticate. Please try logging in.')
            return redirect('signup')


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        return reverse_lazy('edit_profile')  # Redirect to profile page after login


@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    # Initialize review_form to ensure it's available for both GET and POST requests
    review_form = None  # Default to None to handle cases where no review form is present

    if request.method == 'POST':
        # Handle Profile form submission
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile details have been saved.')
            return redirect('edit_profile')
        else:
            messages.error(request, 'Please correct the errors below.')


    else:
        # Initialize form instances for GET request
        form = ProfileForm(instance=profile)
        review_form = ReviewForm()  # Initialize  an empty form

    # Fetch booked workshops
    booked_workshops = Booking.objects.filter(user=request.user).select_related('workshop')

    context = {
        'profile': profile,
        'form': form,
        'review_form': review_form,
        'booked_workshops': booked_workshops,
    }

    return render(request, 'accounts/edit_profile.html', context)


@login_required
def profile(request):
    return render(request, 'accounts/edit_profile.html')


@login_required
def cancel_workshop(request, booking_id):
    user = request.user
    # Ensure the request method is POST (for security reasons)
    if request.method == 'POST':
        # Fetch the booking instance
        booking = get_object_or_404(Booking, id=booking_id)

        # Optionally: Check if the booking belongs to the current user
        if booking.user != request.user:
            messages.error(request, 'You do not have permission to cancel this booking.')
            return redirect('edit_profile')

        # Update the workshop's status to canceled
        workshop = booking.workshop
        # workshop.is_canceled = True
        workshop.save()

        # Optionally: Remove the booking or mark it as canceled
        booking.delete()  # or booking.is_canceled = True and save()

    # Prepare email content for admin
    admin_subject = f'Workshop Cancellation by {user.get_full_name()}'
    admin_message = render_to_string('emails/admin_cancellation_notification.html',
                                     {'user': user, 'workshop': workshop})
    plain_admin_message = strip_tags(admin_message)

    # Prepare email content for user
    user_subject = 'Workshop Cancellation Confirmation'
    user_message = render_to_string('emails/user_cancellation_confirmation.html', {'user': user, 'workshop': workshop})
    plain_user_message = strip_tags(user_message)

    # Send email notification to admin
    try:
        send_mail(admin_subject, plain_admin_message, settings.DEFAULT_FROM_EMAIL, ['oceanofnotions@gmail.com'],
                  html_message=admin_message)
    except Exception as e:
        messages.error(request, f'Failed to send cancellation email to admin: {e}')

    # Send email notification to user
    try:
        send_mail(user_subject, plain_user_message, settings.DEFAULT_FROM_EMAIL, [user.email],
                  html_message=user_message)
    except Exception as e:
        messages.error(request, f'Failed to send cancellation email to user: {e}')

    messages.success(request, 'Workshop booking canceled successfully.')
    return redirect('edit_profile')


def logout_view(request):
    logout(request)
    return redirect('login')


def book_workshop_view(request):
    all_booked_workshops = Workshop.objects.filter(is_booked=True)
    context = {
        'all_booked_workshops': all_booked_workshops,
    }
    return render(request, 'workshops/workshop_list.html', context)


def submit_review(request):
    if request.method == 'POST':
        workshop_id = request.POST.get('workshop_id')
        if workshop_id:
            workshop = get_object_or_404(Workshop, id=workshop_id)
            existing_review = Review.objects.filter(workshop=workshop, user=request.user).first()
            review_form = ReviewForm(request.POST, instance=existing_review)

            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.user = request.user
                review.workshop = workshop
                review.save()
                messages.success(request, 'Your review has been submitted.')
                return redirect('edit_profile')  # Redirect to the desired page

        messages.error(request, 'Invalid workshop ID.')
        return redirect('edit_profile')  # Redirect to the desired page
    else:
        return redirect('edit_profile')  # Redirect if not POST request
