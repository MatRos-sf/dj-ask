from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from question.models import Question, Answer

class QuestionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='123456789')
        self.user2 = User.objects.create_user(username='testuser2', password='123456789')
        self.profile = self.user.profile
        self.profile2 = self.user2.profile

        self.question = Question.objects.create(
            question='test question',
            sender=self.profile,
            receiver=self.profile2,
        )

    def test_can_edit(self):
        self.assertTrue(self.question.can_edit())

        self.question.answer_set.create(answer='test answer', user=self.profile2)
        self.question.refresh_from_db()
        self.assertFalse(self.question.can_edit())


class AnswerModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='123456789')
        self.user2 = User.objects.create_user(username='testuser2', password='123456789')
        self.profile = self.user.profile
        self.profile2 = self.user2.profile

        self.question = Question.objects.create(
            question='test question',
            sender=self.profile,
            receiver=self.profile2,
        )

    def test_save_answer(self):
        # Test that the answer can be saved
        answer = Answer(question=self.question, answer='test answer', user=self.profile2)
        answer.save()
        self.assertEqual(self.question.answer_set.count(), 1)
        self.assertEqual(self.question.answer_set.first().answer, 'test answer')

    def test_cant_answer_twice(self):
        # Test that the user can't answer the same question twice
        answer = Answer(question=self.question, answer='test answer', user=self.profile2)
        answer.save()
        with self.assertRaises(ValidationError):
            answer2 = Answer(question=self.question, answer='test answer 2', user=self.profile2)
            answer2.save()

    def test_cant_answer_to_others_question(self):
        # Test that the user can't answer to other users question
        other_user = User.objects.create_user(username='otheruser', password='1234566789')
        other_user = other_user.profile
        with self.assertRaises(ValidationError):
            answer = Answer(question=self.question, answer='test answer', user=other_user)
            answer.save()

    def test_cant_answer_to_own_question(self):
        # Test that the user can't answer to own question
        with self.assertRaises(ValidationError):
            answer = Answer(question=self.question, answer='test answer', user=self.profile)
            answer.save()