from django.urls import path
from django.conf import settings
from .views import CustomLoginView, SignUpView, edit_profile, Profile
from django.conf.urls.static import static

urlpatterns = [
   path('signup/', SignUpView.as_view(), name='signup'),
   path('login/', CustomLoginView.as_view(), name='login'),
   path('edit-profile/', edit_profile, name='edit_profile'),
   path('profile/', Profile, name='Profile'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
