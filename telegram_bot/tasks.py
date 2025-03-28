from celery import shared_task
from celery.schedules import crontab
from .bot import send_telegram_message
from habits.models import Habit
from datetime import datetime


@shared_task
def send_habit_reminders():
    current_time = datetime.now().time()
    habits = Habit.objects.filter(time__hour=current_time.hour,
                                  time__minute=current_time.minute)

    for habit in habits:
        if hasattr(habit.user, 'profile') and habit.user.profile.telegram_chat_id:
            message = f"Time to {habit.action} at {habit.place}!"
            send_telegram_message(habit.user.profile.telegram_chat_id, message)


from django_celery_beat.models import PeriodicTask, CrontabSchedule


def setup_periodic_tasks(sender, **kwargs):
    schedule, _ = CrontabSchedule.objects.get_or_create(
        minute='*',
        hour='*',
        day_of_week='*',
        day_of_month='*',
        month_of_year='*',
    )

    PeriodicTask.objects.get_or_create(
        crontab=schedule,
        name='Send habit reminders every minute',
        task='telegram_bot.tasks.send_habit_reminders',
    )


from django.db.models.signals import post_migrate

post_migrate.connect(setup_periodic_tasks, sender=None)
