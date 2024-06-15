from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school_details = models.TextField(blank=True)
    students_info = models.TextField(blank=True)

    def __str__(self):
        return f'Profile of {self.user.username}'
from django.db import models

