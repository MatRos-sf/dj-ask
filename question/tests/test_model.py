from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth.models import User
# Create your tests here.
from question.models import Question, Answer
from user.models import Profile
class CreateTest(TestCase):
    def setUp(self) -> None:
        self.user1 = User.objects.create_user(username='user1', password='12345asG')
        self.user2 = User.objects.create_user(username='user2', password='12345asG')

        self.user1 = self.user1.profile
        self.user2 = self.user2.profile
    def test_create_question(self):

        Question.objects.create(
            question="How you doing?",
            sender=self.user1,
            receiver= self.user2
        )
        Question.objects.create(
            question="Do you like blue?",
            sender=self.user1,
            receiver= self.user2
        )

        self.assertEqual(Question.objects.count(), 2)

    def test_check_detail_question(self):
        Question.objects.create(
            question="How you doing?",
            sender=self.user1,
            receiver= self.user2
        )
        Question.objects.create(
            question="Do you like blue?",
            sender=self.user1,
            receiver= self.user2
        )

        # check q1
        q = Question.objects.first()
        q_u2 = self.user2.questions.get(id=1)
        self.assertEqual(q.question, q_u2.question)
        self.assertEqual(q.created, q_u2.created)

    def test_answered_model(self):
        q = Question.objects.create(
            question="How you doing?",
            sender=self.user1,
            receiver= self.user2
        )

        Answer.objects.create(question=q, answer="OK, and you?",
                              user=self.user2)

        self.assertEqual(Answer.objects.count(), 1)

        try:
            # Answer.objects.create(question=q, answer="OK, and you?",
            #                       user=self.user1)
            Answer.objects.create(question=q, answer="OK, and you?",
                                  user=self.user2)
        except ValidationError:
            pass
        self.assertEqual(Answer.objects.count(), 1)
