import os

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.files.storage import default_storage
from django.http import HttpResponse, HttpRequest
from django.views.generic import TemplateView, CreateView, ListView, UpdateView
from django.shortcuts import redirect
from django.utils.html import strip_tags
from django.urls import reverse_lazy


from typing import Any

from .models import (
    Lesson, Olimpiad, StudentProfile,
    SoftSkillTest, Answer, SoftSkillUser
)

from .utils import (
    Importer
)

from .forms import (
    SignUpForm, ProfileEditForm
)


class AllTestView(LoginRequiredMixin, ListView):
    template_name = 'home/test_all.html'
    model = SoftSkillTest
    context_object_name = 'tests'


class TestView(LoginRequiredMixin, TemplateView):
    template_name = 'home/test.html'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        test = SoftSkillTest.objects.get(pk=self.kwargs['pk'])
        questions = test.questions.all()
        answers = Answer.objects.filter(question__in=questions)
        context = super().get_context_data(**kwargs)
        context['page'] = test
        context['questions'] = questions
        context['answers'] = answers
        return context

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        test = SoftSkillTest.objects.get(pk=self.kwargs['pk'])
        questions = test.questions.all()
        answers = Answer.objects.filter(question__in=questions)

        # Получаем ответ от пользователя
        payload = request.POST.dict()
        user_answers = {}

        for key, value in payload.items():
            if key.startswith('question-checkbox-'):
                ans_key = int(key.split('-', 3)[2])
                user_answers.setdefault(ans_key, set()).add(value)
            elif key.startswith('question-input-'):
                user_answers[int(key.split('-', 3)[2])] = {value}
            elif key.startswith('question-radio-'):
                user_answers[int(key.split('-', 3)[2])] = {value}

        score = 0
        for question in questions:
            if question.id in user_answers:
                type_answer = question.type_answer
                if type_answer == 'input':
                    user_answer = user_answers[question.id].pop().lower(
                    ).strip().split(',')
                    correct_answer = strip_tags(
                        answers.get(question=question,
                                    correct=True).answer_text
                    ).lower().split(',')
                    correct_answer = [
                        answer.strip() for answer in correct_answer]
                    if len(user_answer) == 1:
                        user_answer = user_answer[0]
                        if user_answer in correct_answer:
                            score += 1
                    else:
                        user_answer = [
                            answer.strip() for answer in user_answer
                        ]
                        for answer in user_answer:
                            if answer in correct_answer:
                                score += 1 / len(correct_answer)
                elif type_answer == 'radio':
                    user_answer = user_answers[question.id].pop()
                    correct_answer = strip_tags(
                        answers.get(question=question,
                                    correct=True).answer_text
                    )
                    if user_answer == correct_answer:
                        score += 1
                elif type_answer == 'checkbox':
                    user_answer = frozenset(user_answers[question.id])
                    correct_answer = frozenset(
                        strip_tags(answer.answer_text)
                        for answer in answers.filter(
                            question=question, correct=True
                        )
                    )
                    score += len(user_answer & correct_answer) / \
                        len(correct_answer)

        student = StudentProfile.objects.get(user=request.user)

        try:
            softskill = SoftSkillUser.objects.get(user=student, softskill=test)
            softskill.softSkillResult = score
        except SoftSkillUser.DoesNotExist:
            softskill = SoftSkillUser(
                user=student, softskill=test, softSkillResult=score
            )
        softskill.save()

        return redirect('profile')


class OlimpiadsView(LoginRequiredMixin, ListView):
    template_name = 'home/olimpiads.html'
    model = Olimpiad
    context_object_name = 'olimpiads'


class OlimpiadView(LoginRequiredMixin, TemplateView):
    template_name = 'home/olimpiad.html'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        olimpiad = Olimpiad.objects.get(pk=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        context['olimpiad'] = olimpiad
        return context


class Home(TemplateView):
    """
    View для страницы "О сайте" на сайте.

    Этот view рендерит шаблон "home/home.html"
    """
    template_name = "home/home.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        # Fetching olympic and lesson data
        olympiads = Olimpiad.objects.all()

        # Preparing data for carousel (grouped by 3)
        olympic_cards = [olympiads[i:i + 3]
                         for i in range(0, len(olympiads), 3)]

        # Fetching data about disciplines
        disciplines = Lesson.objects.all()

        # Fetching data about soft skill tests
        soft_skill_tests = SoftSkillTest.objects.all()

        # Preparing data for soft skill cards (grouped by 3)
        soft_skill_cards = [soft_skill_tests[i:i + 3]
                            for i in range(0, len(soft_skill_tests), 3)]

        # Adding data to the context
        context['olympic_cards'] = olympic_cards
        context['disciplines'] = disciplines
        context['soft_skill_cards'] = soft_skill_cards

        return context


class Contact(TemplateView):
    """
    View для страницы контактов сайта.

    Этот view рендерит шаблон "home/contact.html"
    """
    template_name = "home/contact.html"


class ProfileView(LoginRequiredMixin, TemplateView):
    """
    View для страницы профиля пользователя.

    Этот view рендерит шаблон "home/profile.html"
    """
    template_name = "home/profile.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        try:
            context['profile'] = StudentProfile.objects.get(user=user)
            context['softskills'] = SoftSkillUser.objects.filter(
                user=context['profile'])
        except StudentProfile.DoesNotExist:
            context['profile'] = None
            context['softskills'] = None
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """
    View для редактирования профиля пользователя.

    Этот view рендерит шаблон "home/profile_edit.html"
    """
    model = StudentProfile
    template_name = "home/profile_edit.html"
    success_url = reverse_lazy('profile')
    form_class = ProfileEditForm

    def get_object(self, queryset=None) -> StudentProfile:
        return self.request.user.student_profile

    def form_valid(self, form: ProfileEditForm) -> HttpResponse:
        user = self.request.user
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save()
        return super().form_valid(form)


class OlimpiadAdminImportView(LoginRequiredMixin, TemplateView):
    """
    View для импорта данных об олимпиадах.

    Этот view рендерит шаблон "home/olimpiads_import.html"
    """
    template_name = "wagtailadmin/olimpiad/import.html"

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if not request.user.is_superuser:
            return redirect('home')
        file = request.FILES.get('file')
        if file and file.name.split('.')[-1] in ['xlsx', 'csv', 'json']:
            file_path = default_storage.save(file.name, file)
            file_path = os.path.join(settings.MEDIA_ROOT, file_path)
            importer = Importer(file_path)
            importer.import_data()
            importer.create_olimpiads()
            os.remove(file_path)
        return redirect('wagtailadmin_home')


class EmailLoginView(LoginView):
    template_name = 'login.html'

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        # Копируем данные запроса, чтобы изменить их
        post_data = request.POST.copy()
        # Переносим данные из поля email в поле username
        post_data['username'] = post_data['email']
        # Обновляем объект POST запроса
        request.POST = post_data
        return super().post(request, *args, **kwargs)


class RegisterView(CreateView):
    """
    View для регистрации нового пользователя.

    Этот view рендерит шаблон "home/register.html"
    """
    model = User
    template_name = "home/register.html"
    form_class = SignUpForm
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form: SignUpForm) -> HttpResponse:
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return response
