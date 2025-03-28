from django.test import TestCase
from habits.models import Habit
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class HabitModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_habit_creation(self):
        habit = Habit.objects.create(
            user=self.user,
            place="Home",
            time="08:00",
            action="Drink water",
            duration=60
        )
        self.assertEqual(str(habit), "Drink water at 08:00:00 in Home")

    def test_duration_validation(self):
        habit = Habit(
            user=self.user,
            place="Home",
            time="08:00",
            action="Drink water",
            duration=150
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()
