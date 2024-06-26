from django.urls import path
from django.conf import settings
from .views import CustomLoginView, SignUpView, edit_profile, cancel_workshop  # Add cancel_workshop
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('cancel-workshop/<int:workshop_id>/', views.cancel_workshop, name='cancel_workshop'),  # Use cancel_workshop directly
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
