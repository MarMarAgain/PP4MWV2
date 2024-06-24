# accounts/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, authenticate
from accounts.forms import CustomUserCreationForm, ProfileForm
from .models import Profile

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')  # Redirect to login page after successful signup
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        # Authenticate the user and login
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(self.request, user)
        return super().form_valid(form)

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        return reverse_lazy('landing_page')

@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('edit_profile')  # Redirect to edit_profile page
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'accounts/../templates/user/edit_profile.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')
