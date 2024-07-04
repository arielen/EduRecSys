from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from apps.home.forms import ProfileEditForm
from apps.home.models import StudentProfile, Olimpiad, Lesson, Mark


class HomeViewTests(TestCase):
    def setUp(self) -> None:
        # Создаем клиента для отправки HTTP-запросов
        self.client = Client()
        # Создаем тестовую запись олимпиады
        Olimpiad.objects.create(name="Math Physiad")
        # Создаем тестовую запись урока
        Lesson.objects.create(lessonName="Mathematics")

    def test_home_view_status_code(self):
        # Отправляем GET-запрос к домашней странице
        response = self.client.get(reverse('home'))
        # Проверяем, что статус-код ответа 200 (ОК)
        self.assertEqual(response.status_code, 200)

    def test_home_view_template_used(self):
        # Отправляем GET-запрос к домашней странице
        response = self.client.get(reverse('home'))
        # Проверяем, что используется правильный шаблон
        self.assertTemplateUsed(response, 'home/home.html')

    def test_home_view_context_data(self):
        # Отправляем GET-запрос к домашней странице
        response = self.client.get(reverse('home'))
        # Проверяем, что контекст содержит ключ 'olympic_cards'
        self.assertIn('olympic_cards', response.context)
        # Проверяем, что контекст содержит ключ 'disciplines'
        self.assertIn('disciplines', response.context)
        # Проверяем, что в контексте есть одна запись олимпиады
        self.assertEqual(len(response.context['olympic_cards']), 1)
        # Проверяем, что в контексте есть одна запись урока
        self.assertEqual(len(response.context['disciplines']), 1)


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
        self.assertTemplateUsed(response, 'home/register.html')

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
        self.assertTemplateUsed(response, 'home/profile_edit.html')
        # Проверка, что форма передана в контекст
        self.assertIsInstance(response.context['form'], ProfileEditForm)


class MarkViewTests(TestCase):

    def setUp(self):
        # Создание тестового пользователя, профиля и урока
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.profile = StudentProfile.objects.create(
            user=self.user, classNumber=10)
        self.lesson = Lesson.objects.create(lessonName='Math')
        self.mark = Mark.objects.create(
            user=self.profile, lesson=self.lesson, mark=5)

    def test_mark_create_view(self):
        # Логин пользователя
        self.client.login(username='testuser', password='testpassword')
        # Создаение нового урока
        new_lesson = Lesson.objects.create(lessonName='English')
        # URL для создания оценки
        url = reverse('mark-create')
        # Данные для создания оценки
        data = {'lesson': new_lesson.id, 'mark': 4, }
        # Отправка POST-запроса на создание оценки
        response = self.client.post(url, data)
        # Проверка перенаправления на success_url
        self.assertRedirects(response, f"{reverse('profile')}#schoolMark")
        # Проверка, что оценка была создана
        self.assertTrue(Mark.objects.filter(user=self.profile,
                        lesson=new_lesson, mark=4).exists())

    def test_mark_update_view(self):
        # Логин пользователя
        self.client.login(username='testuser', password='testpassword')
        # URL для редактирования оценки
        url = reverse('mark-edit', kwargs={'pk': self.mark.lesson.id})
        # Данные для обновления оценки
        data = {'mark': 3, }
        # Отправка POST-запроса на редактирование оценки
        response = self.client.post(url, data)
        # Проверка перенаправления на success_url
        self.assertRedirects(response, f"{reverse('profile')}#schoolMark")
        # Обновление объекта из базы данных
        self.mark.refresh_from_db()
        # Проверка, что данные были обновлены
        self.assertEqual(self.mark.mark, 3)

    def test_mark_delete_view(self):
        # Логин пользователя
        self.client.login(username='testuser', password='testpassword')
        # URL для удаления оценки
        url = reverse('mark-delete', kwargs={'pk': self.mark.lesson.id})
        # Отправка POST-запроса на удаление оценки
        response = self.client.post(url)
        # Проверка перенаправления на success_url
        self.assertRedirects(response, f"{reverse('profile')}#schoolMark")
        # Проверка, что оценка была удалена
        self.assertFalse(Mark.objects.filter(id=self.mark.id).exists())
