from django.urls import path
from .views import CustomLoginView, SignUpView, edit_profile, Profile

urlpatterns = [
   path('signup/', SignUpView.as_view(), name='signup'),
   path('login/', CustomLoginView.as_view(), name='login'),
   path('edit-profile/', edit_profile, name='edit_profile'),
   path('profile/', Profile, name='Profile'),
]
