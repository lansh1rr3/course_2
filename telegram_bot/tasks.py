from celery import shared_task
from .bot import send_telegram_message
from habits.models import Habit
from datetime import datetime


@shared_task
def send_habit_reminders():
    current_time = datetime.now().time()
    habits = Habit.objects.filter(time__hour=current_time.hour,
                                  time__minute=current_time.minute)

    for habit in habits:
        message = f"Time to {habit.action} at {habit.place}!"
        send_telegram_message(habit.user.profile.telegram_chat_id, message)
