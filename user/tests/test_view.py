from django.test import TestCase, Client
from django.contrib.auth.models import User
from time import sleep

class UserTest(TestCase):
    def setUp(self) -> None:
        User.objects.create_user(username='test1', password='Dr3ssCode')
        self.client = Client()
    # def test_login(self):
    #     c = Client()
    #     response = c.post('/login/', {
    #         'username': 'test1',
    #         'password': 'Dr3ssCode'
    #     })
    #     self.assertEqual(response.status_code, 200)
    def test_home(self):
        self.client.login(username='test1', password='Dr3ssCode')
        response = self.client.get('')
        print(response.content)
