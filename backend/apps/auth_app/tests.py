from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .models import StudentProfile
from .forms import ProfileEditForm


class ProfileEditViewTest(TestCase):

    def setUp(self):
        # Создание тестового пользователя и профиля
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.profile = StudentProfile.objects.create(
            user=self.user, classNumber=10)

    def test_profile_edit_view(self):
        # Логин пользователя
        self.client.login(username='testuser', password='testpassword')
        # URL для редактирования профиля
        url = reverse('profile-edit')
        # Данные для обновления профиля
        data = {
            'first_name': 'UpdatedFirstName',
            'last_name': 'UpdatedLastName',
            'classNumber': 11,  # Обновление поля classNumber
        }
        # Отправка POST-запроса на редактирование профиля
        response = self.client.post(url, data)
        # Проверка перенаправления на success_url
        self.assertRedirects(response, reverse('profile'))
        # Обновление объектов из базы данных
        self.user.refresh_from_db()
        self.profile.refresh_from_db()
        # Проверка, что данные были обновлены
        self.assertEqual(self.user.first_name, 'UpdatedFirstName')
        self.assertEqual(self.user.last_name, 'UpdatedLastName')
        self.assertEqual(self.profile.classNumber, 11)

    def test_profile_edit_view_renders_correct_template(self):
        # Логин пользователя
        self.client.login(username='testuser', password='testpassword')
        # URL для редактирования профиля
        url = reverse('profile-edit')
        # GET-запрос к странице редактирования
        response = self.client.get(url)
        # Проверка, что используется правильный шаблон
        self.assertTemplateUsed(response, 'auth/profile_edit.html')
        # Проверка, что форма передана в контекст
        self.assertIsInstance(response.context['form'], ProfileEditForm)


class RegisterViewTests(TestCase):

    def test_register_view_status_code(self):
        # Отправляем GET-запрос к странице регистрации
        response = self.client.get(reverse('register'))
        # Проверяем, что статус-код ответа 200 (ОК)
        self.assertEqual(response.status_code, 200)

    def test_register_view_template_used(self):
        # Отправляем GET-запрос к странице регистрации
        response = self.client.get(reverse('register'))
        # Проверяем, что используется правильный шаблон
        self.assertTemplateUsed(response, 'auth/register.html')

    def test_register_view_form_valid(self):
        # Отправляем POST-запрос с валидными данными для регистрации
        response = self.client.post(reverse('register'), {
            'email': 'QpP3kss@example.com',
            'first_name': 'newuser',
            'last_name': 'newuser',
            'classNumber': 6,
            'sex': True,
            'password1': 'dsuicd9acno23cin',
            'password2': 'dsuicd9acno23cin'
        })
        # Проверяем, что пользователь был создан
        self.assertEqual(User.objects.count(), 1)
        # Проверяем, что созданный пользователь существует в базе данных
        self.assertTrue(
            User.objects.filter(email='QpP3kss@example.com').exists()
        )
        # Проверяем, что ответ перенаправляет (редирект)
        self.assertEqual(response.status_code, 302)

    def test_register_view_form_invalid(self):
        # Отправляем POST-запрос с невалидными данными для регистрации
        response = self.client.post(reverse('register'), {
            'email': 'novalid@example.com',
            'password1': 'password123',
            'password2': 'password'
        })
        # Проверяем, что статус-код ответа 200 (форма отображается снова)
        self.assertEqual(response.status_code, 200)
        # Проверяем, что пользователь не был создан
        self.assertFalse(User.objects.filter(
            email='novalid@example.com').exists())
