from django.db import models
from django.utils import timezone
from transformers.models import Transformer
from users.models import UserAccount


class Collection(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='collections')
    name = models.CharField(max_length=50)
    public = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name + ' - ' + self.name


class CollectionItem(models.Model):
    class Priorities(models.TextChoices):
        HIGHEST = 1
        HIGH = 2
        MEDIUM = 3
        LOW = 4
        LOWEST = 5
    
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='items')
    transformer = models.ForeignKey(Transformer, on_delete=models.CASCADE)
    priority = models.PositiveIntegerField(choices=Priorities.choices, null=True, default=None)
    date = models.DateField(default=timezone.now)
    
    def __str__(self):
        return str(self.transformer)
    