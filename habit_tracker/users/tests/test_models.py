from django.test import TestCase
from django.contrib.auth.models import User
from users.models import Profile

class ProfileModelTest(TestCase):
    def test_profile_creation(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        self.assertTrue(hasattr(user, 'profile'))
        self.assertEqual(user.profile.telegram_chat_id, None)

    def test_profile_str(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        self.assertEqual(str(user.profile), "Profile for testuser")