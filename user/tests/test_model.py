from django.test import TestCase

from django.contrib.auth.models import User
from user.models import Profile
class CreateTest(TestCase):
    def setUp(self) -> None:
        User.objects.create_user(username="test", password='1234qwesdfxcvF')

    def test_signal_profile(self):

        self.assertEqual(Profile.objects.count(), 1)

    def test_create_random_qty_user(self):
        from random import randint

        qty = randint(1, 13)
        for i in range(qty):
            User.objects.create_user(username=f"test{i}", password='1234qwesdfxcvF')

        self.assertEqual(User.objects.count(), Profile.objects.count())
        self.assertEqual(qty+1, Profile.objects.count())

