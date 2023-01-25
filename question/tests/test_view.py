from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client

from question.models import Question, Answer

class QueAnsViewsTest(TestCase):
    def setUp(self) -> None:
        user1 = User.objects.create_user(username='test1', password='Dr3ssCode')
        user2 = User.objects.create_user(username='test2', password='Dr3ssCode')

        self.user1 = user1.profile
        self.user2 = user2.profile
        self.client = Client()

    def test_create_question_view(self):
        self.client.login(username='test1', password='Dr3ssCode')
        response = self.client.post(reverse('question:create'), {
            'question': 'you ok?',
            'receiver': 2,
            'anonymous': False
        })

        self.assertEqual(Question.objects.count(), 1)
        obj = Question.objects.get(id=1)

        self.assertEqual(obj.question, 'you ok?')
        self.assertEqual(obj.sender, self.user1)
        self.assertEqual(obj.receiver, self.user2)
        self.assertEqual(obj.anonymous, False)

    def test_delete_question_view(self):
        self.client.login(username='test1', password='Dr3ssCode')
        Question.objects.create(
            question="How you doing?",
            sender=self.user1,
            receiver= self.user2
        )
        response = self.client.get(reverse('question:delete', kwargs={'pk': 1}))

        self.assertEqual(Question.objects.count(), 0)




