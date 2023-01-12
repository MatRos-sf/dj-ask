from django.test import TestCase

from django.contrib.auth.models import User
from user.models import Profile
from question.models import Question, Answer

class SimpleTest(TestCase):
    def setUp(self) -> None:
        # create users
        self.user1 = User.objects.create_user(username="user1", password='1234qwesdfxcvF')
        self.user2 = User.objects.create_user(username="user2", password='1234qwesdfxcvF')

        self.payload = {
            "question": "test?",
            "sender": self.user1.profile,
            "receiver": self.user2.profile
        }
        self.payload2 = {
            "question": "test? ok?",
            "sender": self.user1.profile,
            "receiver": self.user2.profile
        }

    def test_ask_question_user1(self):
        q = Question.objects.create(
            **self.payload
        )
        q2 = Question.objects.create(
            **self.payload2
        )

        self.assertEqual(Question.objects.count(),2)

    def test_ask_question_and_answered(self):
        q = Question.objects.create(
            **self.payload
        )
        q2 = Question.objects.create(
            **self.payload2
        )

        Answer.objects.create(
            question = q,
            answer = "OK TEST",
            user = self.user2.profile
        )

        self.assertEqual(Answer.objects.count(), 1)
        # check
        self.assertEqual(
            self.user2.profile.qty_asked(), 0
        )
        self.assertEqual(
            self.user1.profile.qty_asked(), 2
        )
        self.assertEqual(
            self.user1.profile.qty_answered(), 0
        )
        self.assertEqual(
            self.user2.profile.qty_answered(), 1
        )

