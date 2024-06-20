#accounts/views.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from accounts.forms import CustomUserCreationForm, ProfileForm


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

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

@login_required
def Profile(request):
   return render(request, 'accounts/profile.html')