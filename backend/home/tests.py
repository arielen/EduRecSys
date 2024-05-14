from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import Olimpiad, Lesson


class AboutViewTests(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        Olimpiad.objects.create(name="Math Olympiad")
        Lesson.objects.create(lessonName="Mathematics")

    def test_about_view_status_code(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_about_view_template_used(self):
        response = self.client.get(reverse('about'))
        self.assertTemplateUsed(response, 'home/about.html')

    def test_about_view_context_data(self):
        response = self.client.get(reverse('about'))
        self.assertIn('cards', response.context)
        self.assertIn('disciplines', response.context)
        self.assertEqual(len(response.context['cards']), 1)
        self.assertEqual(len(response.context['disciplines']), 1)


class ContactViewTests(TestCase):

    def test_contact_view_status_code(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)

    def test_contact_view_template_used(self):
        response = self.client.get(reverse('contact'))
        self.assertTemplateUsed(response, 'home/contact.html')


class RegisterViewTests(TestCase):

    def test_register_view_status_code(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_register_view_template_used(self):
        response = self.client.get(reverse('register'))
        self.assertTemplateUsed(response, 'home/register.html')

    def test_register_view_form_valid(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'password123',
            'password2': 'password123'
        })
        self.assertEqual(User.objects.count(), 1)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertEqual(response.status_code, 302)  # Проверка на редирект

    def test_register_view_form_invalid(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'password123',
            'password2': 'password'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='newuser').exists())
