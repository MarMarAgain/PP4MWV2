from django.contrib.auth.models import User
from django.db import models
from workshops.models import Workshop
from django.contrib.auth.models import User

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'user_{instance.user.id}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    school_details = models.TextField(blank=True)
    students_info = models.TextField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    booked_workshops = models.ManyToManyField(Workshop, blank=True)

    def __str__(self):
        return self.user.username

