from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telegram_chat_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Profile for {self.user.username}"
