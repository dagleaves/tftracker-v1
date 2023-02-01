from django.db import models
from users.models import UserAccount


class UserPreferences(models.Model):
    class DisplayPreferences(models.TextChoices):
        EVERYONE = 'E'
        FRIENDS_ONLY = 'F'
        NO_ONE = 'N'

    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    
    real_name = models.CharField(
        max_length=1, 
        choices=DisplayPreferences.choices, 
        default=DisplayPreferences.NO_ONE)

    gender = models.CharField(
        max_length=1, 
        choices=DisplayPreferences.choices, 
        default=DisplayPreferences.NO_ONE)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name
