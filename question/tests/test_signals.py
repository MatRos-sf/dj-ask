from django.test import TestCase
from django.contrib.auth.models import User

from question.models import Question, Answer

class QueAnsSignalTest(TestCase):
    def setUp(self) -> None:
        # create user
        user1 = User.objects.create_user(username='user1', password='1234qwerGH')
        self.user1 = user1.profile
        user2 = User.objects.create_user(username='user2', password='1234qwerGH')
        self.user2 = user2.profile
        # create Question

        self.q1 = Question.objects.create(
            question = 'You OK ?',
            sender = self.user1,
            receiver = self.user2
        )
        self.q2 = Question.objects.create(
            question = 'Do you like pizza ?',
            sender = self.user2,
            receiver = self.user1
        )

    def test_answer_create_signal(self):
        Answer.objects.create(
            question = self.q1,
            answer = "So so and you?",
            user = self.user2
        )

        self.assertEqual(
            Question.objects.get(id=1).is_answer, 1
        )
        self.assertEqual(
            Question.objects.get(id=2).is_answer,2
        )

    def test_answer_delete_signal(self):
        a1= Answer.objects.create(
            question = self.q1,
            answer = "So so and you?",
            user = self.user2
        )

        a1.delete()
        self.assertEqual(
            Question.objects.get(id=1).is_answer, 2
        )
