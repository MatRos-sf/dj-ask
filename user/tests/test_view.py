from django.test import TestCase, Client
from django.contrib.auth.models import User
from time import sleep

class UserTest(TestCase):
    def setUp(self) -> None:
        User.objects.create_user(username='test1', password='Dr3ssCode')
        self.client = Client()

    def test_home(self):
        self.client.login(username='test1', password='Dr3ssCode')
        response = self.client.get('')
        context = response.context.dicts[-1]
        context_rando = context.get('rando', None)
        context_friends = context.get('rando_friends', None)

        self.assertIsNotNone(context_rando,context_friends)
