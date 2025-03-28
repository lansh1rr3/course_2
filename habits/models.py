from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class Habit(models.Model):
    FREQUENCY_CHOICES = [
        (1, 'Daily'),
        (2, 'Every 2 days'),
        (3, 'Every 3 days'),
        (4, 'Every 4 days'),
        (5, 'Every 5 days'),
        (6, 'Every 6 days'),
        (7, 'Weekly'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.CharField(max_length=100)
    time = models.TimeField()
    action = models.CharField(max_length=200)
    is_pleasant = models.BooleanField(default=False)
    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'is_pleasant': True}
    )
    frequency = models.PositiveIntegerField(
        choices=FREQUENCY_CHOICES,
        default=1
    )
    reward = models.CharField(max_length=200, null=True, blank=True)
    duration = models.PositiveIntegerField()
    is_public = models.BooleanField(default=False)

    def clean(self):
        if self.reward and self.related_habit:
            raise ValidationError("Cannot set both reward and related habit")
        if self.duration > 120:
            raise ValidationError("Duration cannot exceed 120 seconds")
        if self.is_pleasant and (self.reward or self.related_habit):
            raise ValidationError("Pleasant habit cannot have reward or related habit")
        if self.frequency > 7:
            raise ValidationError("Frequency cannot be less than once a week")

    def __str__(self):
        return f"{self.action} at {self.time} in {self.place}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telegram_chat_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Profile for {self.user.username}"


from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
