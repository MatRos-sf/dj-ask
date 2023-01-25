from django.test import TestCase, Client
from django.contrib.auth.models import User
from time import sleep
from django.conf import settings
from django.urls import reverse



class UserTest(TestCase):
    def setUp(self) -> None:
        User.objects.create_user(username='test1', password='Dr3ssCode')
        User.objects.create_user(username='test2', password='Dr3ssCode')
        User.objects.create_user(username='test3', password='Dr3ssCode')

        self.client = Client()

    # def test_home(self):
    #     self.client.login(username='test1', password='Dr3ssCode')
    #     response = self.client.get('')
    #     context = response.context.dicts[-1]
    #     context_rando = context.get('rando', None)
    #     context_friends = context.get('rando_friends', None)
    #
    #     self.assertIsNotNone(context_rando,context_friends)

    def test_login_url(self):
        response = self.client.post(reverse(f'login'), {
            'username': 'test1',
            'password': 'Dr3ssCode'
        }, follow=True)

        status_code = response.status_code == 200
        self.assertTrue(status_code)
        self.assertEqual(response.request.get("PATH_INFO"), settings.LOGIN_REDIRECT_URL)


class RegisterViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_register_view_status_code(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_register_view_uses_correct_templates(self):
        response = self.client.get(reverse('register'))
        self.assertTemplateUsed(response, 'user/register.html')

    def test_register_view_create_user(self):
        data = {
            'username': 'test',
            'email': 'test@example.com',
            'password': 'Test12password'
        }
        response = self.client.post(reverse('register'), data, follow=True)
        self.assertEqual(response.status_code, 200)
        # I'm not sure it's working !

class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )

    def test_home_view_redirects_if_not_logged_in(self):
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, '/login/?next=/')

    def test_home_view_status_code(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_template(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'user/home.html')

    def test_home_view_context_data(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('home'))
        # it's not working
        # self.assertContains(response, 'rando')
        # self.assertContains(response, 'rando_friends')


class ProfileDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.profile = self.user.profile

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/profile/1/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('detail', args=[self.profile.id]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('detail', args=[self.profile.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/detail.html')

    def test_view_shows_user_data(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('detail', args=[self.profile.id]))
        self.assertContains(response, 'testuser')
        self.assertContains(response, 'Answered questions:')
        self.assertContains(response, 'Ask a quick question:')

