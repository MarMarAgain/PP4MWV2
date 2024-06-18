from django.urls import path
from .views import SignUpView, edit_profile, profile

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('profile/', profile, name='profile'),
]
