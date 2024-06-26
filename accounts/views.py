# accounts/views.py

from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from accounts.forms import CustomUserCreationForm, ProfileForm
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404
from workshops.models import Workshop, Booking
from django.contrib.auth.decorators import login_required
from django.conf import settings


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')  # Redirect to profile page after successful signup
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        # Save the user and authenticate
        user = form.save(commit=False)
        raw_password = form.cleaned_data.get('password1')
        user.set_password(raw_password)  # Set password properly
        user.full_name = form.cleaned_data.get('full_name')  # Save full_name to User model
        user.phone_number = form.cleaned_data.get('phone_number')  # Save phone_number to User model
        user.save()

        # Authenticate the user and login
        user = authenticate(username=user.username, password=raw_password)
        if user is not None:
            login(self.request, user)
            messages.success(self.request, 'Account created successfully!')
            return redirect(self.success_url)
        else:
            messages.error(self.request, 'Failed to authenticate. Please try logging in.')
            return redirect('signup')
        #login(self.request, user)

        #return super().form_valid(form)

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        return reverse_lazy('edit_profile')  # Redirect to profile page after login

@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            print("Form is valid")
            print("Uploaded file:", request.FILES.get('profile_picture'))
            form.save()
            messages.success(request, 'Your profile details have been saved.')
            return redirect('edit_profile')  # Redirect after successful form submission
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileForm(instance=profile)

    context = {
        'profile': profile,
        'form': form,
    }

    return render(request, 'accounts/edit_profile.html', context)



@login_required
def profile(request):
    return render(request, 'accounts/edit_profile.html')



@login_required
def cancel_workshop(request, workshop_id):
    workshop = get_object_or_404(Workshop, pk=workshop_id)

    # Remove the workshop from user's booked workshops
    request.user.profile.booked_workshops.remove(workshop)

    # Send email notification to admin
    subject = f'Workshop Cancellation by {request.user.get_full_name()}'
    message = f'The user {request.user.get_full_name()} has canceled the workshop: {workshop.title}'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, ['oceanofnotions@gmail.com'])

    messages.success(request, 'Workshop booking canceled successfully.')
    return redirect('edit_profile')
