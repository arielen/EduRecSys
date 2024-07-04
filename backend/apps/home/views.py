import os

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.files.storage import default_storage
from django.db.models import Exists, OuterRef, Avg, Q
from django.http import HttpResponse, HttpRequest
from django.views.generic import (
    TemplateView, CreateView, ListView, UpdateView, DeleteView
)
from django.shortcuts import get_object_or_404, redirect
from django.utils.html import strip_tags
from django.urls import reverse, reverse_lazy


from typing import Any, TypeVar

from .models import (
    Lesson, Olimpiad, StudentProfile,
    SoftSkillTest, Answer, SoftSkillUser, Mark,
    AdditionalOlimpiadLesson, BaseOlimpiadLesson, OlimpiadSS
)

from .utils import (
    Importer
)

from .forms import (
    SignUpForm, ProfileEditForm,
)

OlimpiadLesson = TypeVar(
    'OlimpiadLesson',
    BaseOlimpiadLesson,
    AdditionalOlimpiadLesson
)


class AdviceView(LoginRequiredMixin, TemplateView):
    template_name = 'home/advice.html'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user_profile = self.request.user.student_profile

        user_marks = Mark.objects.filter(user=user_profile) \
            .select_related('lesson')
        lessons = user_marks.values_list('lesson', flat=True)

        # selected_lesson_id = self.request.GET.get('lesson', None)

        # Fetching Olympiad lessons
        base_olimp_lessons = BaseOlimpiadLesson.objects. \
            filter(lesson__in=lessons).prefetch_related('lesson')
        additional_olimp_lessons = AdditionalOlimpiadLesson.objects. \
            filter(lesson__in=lessons).prefetch_related('lesson')

        # if selected_lesson_id:
        #     base_olimp_lessons = base_olimp_lessons. \
        #         filter(lesson_id=selected_lesson_id)
        #     additional_olimp_lessons = additional_olimp_lessons. \
        #         filter(lesson_id=selected_lesson_id)

        # Filtering recommendations
        def get_recommendations(olimp_lessons: OlimpiadLesson) -> list[OlimpiadLesson]:
            recommendations = []
            for lesson in olimp_lessons:
                avg_mark = user_marks.filter(lesson=lesson.lesson).\
                    aggregate(avg_mark=Avg('mark'))['avg_mark']
                if avg_mark and avg_mark >= lesson.minAvgMarkFor3Years:
                    recommendations.append(lesson)
            return recommendations

        base_recommendations = get_recommendations(base_olimp_lessons)
        additional_recommendations = get_recommendations(
            additional_olimp_lessons)

        # Fetching soft skills
        user_soft_skills = SoftSkillUser.objects.\
            filter(user=user_profile).select_related('softskill')
        softskill_olimpiads = OlimpiadSS.objects.\
            filter(
                ss__in=user_soft_skills.values_list('softskill', flat=True)
            ).prefetch_related('ss')

        softskill_recommendations = []
        for softskill in softskill_olimpiads:
            user_soft_skill = user_soft_skills.filter(
                softskill__softSkill=softskill.ss).last()
            if user_soft_skill \
                    and user_soft_skill.softSkillResult >= softskill.minRezult:
                softskill_recommendations.append(softskill)

        # Filtering final recommendations
        olimpiads_recommendations = Olimpiad.objects.filter(
            Q(baseolimpiadlesson__in=base_recommendations) &
            Q(additionalolimpiadlesson__in=additional_recommendations) &
            Q(olimpiadsoftskill__in=softskill_recommendations)
        ).distinct()

        context['recommendations'] = olimpiads_recommendations
        context['lessons'] = lessons

        return context


class AllTestView(LoginRequiredMixin, ListView):
    template_name = 'home/test_all.html'
    model = SoftSkillTest
    context_object_name = 'tests'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Используем подзапрос для определения, прошел ли пользователь тест
        softSkillUserSubquery = SoftSkillUser.objects.filter(
            user=user.student_profile,
            softskill=OuterRef('pk')
        )
        # Добавляем аннотированные поля к запросу
        context['tests'] = SoftSkillTest.objects.annotate(
            user_passed=Exists(softSkillUserSubquery)
        ).order_by('softSkill__name')
        return context


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
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context['user'] = user

        # Получение профиля студента пользователя
        profile = getattr(user, 'student_profile', None)
        context['profile'] = profile

        if profile:
            # Получение всех мягких навыков пользователя и их идентификаторов за один запрос
            user_softskills = SoftSkillUser.objects.filter(user=profile) \
                .select_related('softskill')
            user_softskills_ids = user_softskills.values_list(
                'softskill_id', flat=True
            )

            # Прямое назначение результатов в контекст
            context['softskills'] = user_softskills.order_by(
                'softskill__softSkill__name')
            # Получение всех мягких навыков и исключение тех, что у пользователя уже есть
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

    Этот view рендерит шаблон "home/profile_edit.html"
    """
    model = StudentProfile
    template_name = "home/profile_edit.html"
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


class MarkCreateView(LoginRequiredMixin, CreateView):
    model = Mark
    fields = ('lesson', 'mark')
    success_url = reverse_lazy('profile')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        filled_lessons = Mark.objects. \
            filter(user=self.request.user.student_profile). \
            values_list('lesson', flat=True)
        form.fields['lesson'].queryset = Lesson.objects.\
            exclude(id__in=filled_lessons). \
            order_by('lessonName')
        return form

    def form_valid(self, form) -> HttpResponse:
        form.instance.user = self.request.user.student_profile
        return super().form_valid(form)

    def get_success_url(self):
        return f"{reverse('profile')}#schoolMark"


class MarkUpdateView(LoginRequiredMixin, UpdateView):
    model = Mark
    fields = ('mark',)
    template_name = 'home/mark_edit.html'

    def get_object(self, queryset=None) -> Mark:
        return get_object_or_404(
            Mark, user=self.request.user.student_profile,
            lesson=self.kwargs['pk'])

    def get_success_url(self):
        return f"{reverse('profile')}#schoolMark"


class MarkDeleteView(LoginRequiredMixin, DeleteView):
    model = Mark

    def get_object(self, queryset=None) -> Mark:
        return get_object_or_404(
            Mark, user=self.request.user.student_profile,
            lesson=self.kwargs['pk'])

    def get_success_url(self):
        return f"{reverse('profile')}#schoolMark"


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

    def dispatch(self, request, *args, **kwargs) -> HttpResponse:
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
