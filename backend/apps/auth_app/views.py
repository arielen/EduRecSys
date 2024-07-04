from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (
    TemplateView, CreateView, UpdateView
)
from django.urls import reverse_lazy

from .forms import ProfileEditForm, SignUpForm
from .models import StudentProfile

from apps.home.models import Mark, SoftSkillTest, SoftSkillUser

from typing import Any


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

    Этот view рендерит шаблон "auth/register.html"
    """
    model = User
    template_name = "auth/register.html"
    form_class = SignUpForm
    success_url = reverse_lazy('home')

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
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


class ProfileView(LoginRequiredMixin, TemplateView):
    """
    View для страницы профиля пользователя.

    Этот view рендерит шаблон "auth/profile.html"
    """
    template_name = "auth/profile.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context['user'] = user

        # Получение профиля студента пользователя
        profile = getattr(user, 'student_profile', None)
        context['profile'] = profile

        if profile:
            # Получение всех мягких навыков пользователя
            # и их идентификаторов за один запрос
            user_softskills = SoftSkillUser.objects.filter(user=profile) \
                .select_related('softskill')
            user_softskills_ids = user_softskills.values_list(
                'softskill_id', flat=True
            )

            # Прямое назначение результатов в контекст
            context['softskills'] = user_softskills.order_by(
                'softskill__softSkill__name')
            # Получение всех мягких навыков и исключение тех,
            # что у пользователя уже есть
            context['missing_softskills'] = SoftSkillTest.objects.exclude(
                id__in=user_softskills_ids
            )

            user_marks = Mark.objects.filter(user=profile) \
                .order_by('lesson__lessonName') \
                .select_related('lesson')
            context['marks'] = user_marks

        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """
    View для редактирования профиля пользователя.

    Этот view рендерит шаблон "auth/profile_edit.html"
    """
    model = StudentProfile
    template_name = "auth/profile_edit.html"
    success_url = reverse_lazy('profile')
    form_class = ProfileEditForm

    def get_object(self, queryset=None) -> StudentProfile:
        # Использование get_object_or_404 для надежности
        return get_object_or_404(StudentProfile, user=self.request.user)

    def form_valid(self, form: ProfileEditForm) -> HttpResponse:
        user = self.request.user
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save()
        return super().form_valid(form)
