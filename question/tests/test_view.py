from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client

from question.models import Question, Answer

# class QueAnsViewsTest(TestCase):
#     def setUp(self) -> None:
#         user1 = User.objects.create_user(username='test1', password='Dr3ssCode')
#         user2 = User.objects.create_user(username='test2', password='Dr3ssCode')
#
#         self.user1 = user1.profile
#         self.user2 = user2.profile
#         self.client = Client()
#
#     def test_create_question_view(self):
#         self.client.login(username='test1', password='Dr3ssCode')
#         response = self.client.post(reverse('question:create'), {
#             'question': 'you ok?',
#             'receiver': 2,
#             'anonymous': False
#         })
#
#         self.assertEqual(Question.objects.count(), 1)
#         obj = Question.objects.get(id=1)
#
#         self.assertEqual(obj.question, 'you ok?')
#         self.assertEqual(obj.sender, self.user1)
#         self.assertEqual(obj.receiver, self.user2)
#         self.assertEqual(obj.anonymous, False)
#
#     def test_delete_question_view(self):
#         self.client.login(username='test1', password='Dr3ssCode')
#         Question.objects.create(
#             question="How you doing?",
#             sender=self.user1,
#             receiver= self.user2
#         )
#         response = self.client.get(reverse('question:delete', kwargs={'pk': 1}))
#
#         self.assertEqual(Question.objects.count(), 0)
#



class RandomQuestionTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='testuser', password='testpassword')
        self.user2 = User.objects.create_user(username='testuser2', password='testpassword')
        self.user3 = User.objects.create_user(username='testuser3', password='testpassword')


        self.profile = self.user1.profile
        self.profile2 = self.user2.profile
        self.profile3 = self.user3.profile


        self.client.login(username='testuser', password='testpassword')

    def test_random_question_to_rando(self):
        # Test random question to random profile
        response = self.client.get(reverse('question:random', kwargs={'name': 'rando'}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Question.objects.count(), 1)
        question = Question.objects.first()
        self.assertEqual(question.sender, self.profile)
        self.assertNotEqual(question.receiver, self.profile)

    def test_random_question_to_friends(self):
        # Test random question to friend
        self.profile.friends.add(self.profile2)
        response = self.client.get(reverse('question:random', kwargs={'name': 'friends'}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Question.objects.count(), 1)
        question = Question.objects.first()
        self.assertEqual(question.sender, self.profile)
        self.assertEqual(question.receiver, self.profile2)

    def test_random_question_to_non_existing_friends(self):
        # Test random question to non-existing friends
        response = self.client.get(reverse('question:random', kwargs={'name': 'friends'}))
        self.assertTemplateUsed(response, "question/info.html")
        self.assertEqual(Question.objects.count(), 0)
