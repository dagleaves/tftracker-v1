from django.db import models
from users.models import UserAccount


class UserProfile(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    avatar = models.ImageField(unique=True, null=True, default=None, upload_to='avatars')
    display_name = models.CharField(max_length=50, default='')
    middle_name = models.CharField(max_length=50, default='')
