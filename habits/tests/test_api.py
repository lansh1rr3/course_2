from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from habits.models import Habit
from rest_framework_simplejwt.tokens import RefreshToken


class HabitAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.other_user = User.objects.create_user(username='otheruser', password='otherpass')
        self.habit = Habit.objects.create(
            user=self.user,
            place="Home",
            time="08:00",
            action="Drink water",
            duration=60
        )
        self.public_habit = Habit.objects.create(
            user=self.other_user,
            place="Park",
            time="09:00",
            action="Run",
            duration=60,
            is_public=True
        )
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_list_habits(self):
        response = self.client.get('/api/habits/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['action'], "Drink water")

    def test_list_public_habits(self):
        response = self.client.get('/api/public-habits/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['action'], "Run")

    def test_create_habit(self):
        data = {
            "place": "Office",
            "time": "10:00",
            "action": "Stretch",
            "duration": 60
        }
        response = self.client.post('/api/habits/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 3)

    def test_update_own_habit(self):
        data = {"action": "Updated action"}
        response = self.client.patch(f'/api/habits/{self.habit.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.action, "Updated action")

    def test_update_other_user_habit(self):
        data = {"action": "Updated action"}
        response = self.client.patch(f'/api/habits/{self.public_habit.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
