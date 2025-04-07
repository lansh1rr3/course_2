from django.test import TestCase
from django.core.exceptions import ValidationError
from habits.models import Habit
from django.contrib.auth.models import User


class HabitValidatorsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_reward_and_related_habit(self):
        pleasant_habit = Habit.objects.create(
            user=self.user,
            place="Home",
            time="08:00",
            action="Relax",
            duration=60,
            is_pleasant=True
        )
        habit = Habit(
            user=self.user,
            place="Home",
            time="08:00",
            action="Drink water",
            duration=60,
            reward="Coffee",
            related_habit=pleasant_habit
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_duration_exceeds_120(self):
        habit = Habit(
            user=self.user,
            place="Home",
            time="08:00",
            action="Drink water",
            duration=150
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_pleasant_habit_with_reward(self):
        habit = Habit(
            user=self.user,
            place="Home",
            time="08:00",
            action="Relax",
            duration=60,
            is_pleasant=True,
            reward="Coffee"
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_frequency_exceeds_7(self):
        habit = Habit(
            user=self.user,
            place="Home",
            time="08:00",
            action="Drink water",
            duration=60,
            frequency=8
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()
