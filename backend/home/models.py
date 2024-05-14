from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from modelcluster.fields import ParentalKey

from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.fields import RichTextField
from wagtail.models import Page, ClusterableModel


class City(models.Model):
    """
    Модель для хранения городов.

    Fields:
        cityName: Название города.
    """
    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"

    cityName = models.CharField(max_length=255, verbose_name='Название города')

    def __str__(self) -> str:
        return self.cityName


class School(models.Model):
    """
    Модель для хранения информации о школе.

    Fields:
        schoolName: Наименование школы.
        city: Город, в котором находится школа.
    """
    class Meta:
        verbose_name = "Школа"
        verbose_name_plural = "Школы"

    schoolName = models.CharField(
        max_length=50, verbose_name='Наименование школы'
    )
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, verbose_name='Город')

    def __str__(self) -> str:
        return self.schoolName


class Lesson(models.Model):
    """
    Модель для хранения информации о дисциплине.

    Fields:
        lessonName: Наименование дисциплины.
    """
    class Meta:
        verbose_name = "Дисциплина"
        verbose_name_plural = "Дисциплины"

    lessonName = models.CharField(
        max_length=50, verbose_name='Наименование дисциплины', unique=True
    )

    def __str__(self) -> str:
        """
        Строковое представление модели.

        :return: наименование дисциплины
        :rtype: str
        """
        return self.lessonName


def create_student_profile(cls):
    """Декоратор для создания экземпляра модели StudentProfile для каждого User"""

    def create_profile(sender, instance, created, **kwargs):
        if created:
            StudentProfile.objects.create(user=instance)

    post_save.connect(create_profile, sender=cls)
    return cls


@create_student_profile
class StudentProfile(models.Model):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='student_profile',
    )
    about = models.TextField(verbose_name='О себе', blank=True, null=True)
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, verbose_name='Город',
        blank=True, null=True
    )
    school = models.ForeignKey(
        School, on_delete=models.CASCADE, verbose_name='Школа',
        blank=True, null=True
    )
    classNumber = models.IntegerField(
        verbose_name='Номер класса',
        choices=[(i, i) for i in range(1, 12)],
        blank=True, null=True
    )
    sex = models.BooleanField(
        verbose_name='Пол', choices=[(True, 'Мужской'), (False, 'Женский')],
        default=True
    )
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, verbose_name='Урок',
        blank=True, null=True
    )
    SNILS = models.CharField(
        max_length=14, verbose_name='СНИЛС', unique=True,
        blank=True, null=True
    )
    startYear = models.DateField(
        verbose_name='Год начала обучения',
        blank=True, null=True
    )

    def __str__(self):
        return f"{self.user.username}'s student profile"


class Mark(models.Model):
    """
    Модель для хранения оценок пользователей по каждому уроку.

    Fields:
        lesson: Урок, который учит пользователь.
        user: Пользователь, которому выставлена оценка.
        mark: Оценка, которая была присвоена.

    """
    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"

    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE,
        verbose_name='Урок'
    )
    user = models.ForeignKey(
        StudentProfile, on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    mark = models.IntegerField(
        verbose_name='Оценка',
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    )

    def __str__(self) -> str:
        return f"{self.user} {self.lesson} {self.mark} {self.class_}"


class Olimpiad(models.Model):
    """
    Модель для хранения информации о конкретной олимпиаде.

    Fields:
        name: Название олимпиады.
        link: Ссылка на олимпиаду.
    """
    class Meta:
        verbose_name = "Олимпиада"
        verbose_name_plural = "Олимпиады"

    name = models.CharField(max_length=50, verbose_name='Название олимпиады')
    link = models.URLField(verbose_name='Ссылка на олимпиаду')

    def __str__(self) -> str:
        return self.name


class OlimpiadLesson(models.Model):
    """
    Модель для хранения информации о связи олимпиады и дисциплины.

    Fields:
        lesson: Урок.
        olimpiad: Олимпиада.
        minRezult: Минимальный результат, который должен получить
            пользователь для прохождения олимпиады по данной дисциплине.
    """
    class Meta:
        verbose_name = "Олимпиада по дисциплине"
        verbose_name_plural = "Олимпиады по дисциплинам"

    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, verbose_name='Урок'
    )
    olimpiad = models.ForeignKey(
        Olimpiad, on_delete=models.CASCADE, verbose_name='Олимпиада'
    )
    minRezult = models.IntegerField(
        verbose_name='Минимальный резултат',
        default=0
    )


class SoftSkill(models.Model):
    """
    Модель для хранения информации о softskill-е.

    Fields:
        name: Наименование softskill-а.
    """
    class Meta:
        verbose_name = "Softskill"
        verbose_name_plural = "Softskills"

    name = models.CharField(
        max_length=50,
        verbose_name='Наименование softskill-а'
    )

    def __str__(self) -> str:
        """
        Строковое представление модели.

        :return: наименование softskill-а
        :rtype: str
        """
        return self.name


class TestSS(models.Model):
    """
    Модель для хранения информации о тесте softskill-а.

    Fields:
        softSkill: softskill-а.
        path: Ссылка на softskill.
    """
    class Meta:
        verbose_name = "Test softskill"
        verbose_name_plural = "Test softskills"

    softSkill = models.ForeignKey(
        SoftSkill, on_delete=models.CASCADE,
        verbose_name='Softskill'
    )
    path = models.URLField(verbose_name='Ссылка на softskill')

    def __str__(self) -> str:
        """
        Строковое представление модели.

        :return: наименование softskill-а
        :rtype: str
        """
        return self.softSkill


class TestSSUserResult(models.Model):
    """
    Модель для хранения информации о результате
    прохождения теста softskill-а пользователем.

    Fields:
        user - пользователь, проходивший тест
        softSkill - тест softskill-а
        softSkillResult - результат прохождения теста
    """
    class Meta:
        verbose_name = "Test softskill result"
        verbose_name_plural = "Test softskill results"

    user = models.ForeignKey(
        StudentProfile, on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    softSkill = models.ForeignKey(
        TestSS, on_delete=models.CASCADE,
        verbose_name='Test Softskill'
    )
    softSkillResult = models.IntegerField(
        verbose_name='Результат softskill',
    )

    def __str__(self) -> str:
        """
        Строковое представление модели.

        :return: наименование пользователя и теста
        :rtype: str
        """
        return f"{self.user} {self.softSkill} {self.softSkillResult}"


class OlimpiadSS(models.Model):
    """
    Модель для хранения информации о том, какой softskill
    присваивается при прохождении Олимпиады.

    Fields:
        ss - softskill при прохождении олимпиады
        olimpiad - олимпиада для которой присваивается softskill
        minRezult - минимальный результат, который необходимо получить
            для получения softskill при прохождении олимпиады
    """
    class Meta:
        verbose_name = "Olimpiad softskill"
        verbose_name_plural = "Olimpiad softskills"

    ss = models.ForeignKey(
        SoftSkill,
        on_delete=models.CASCADE, verbose_name='Softskill'
    )
    olimpiad = models.ForeignKey(
        Olimpiad, on_delete=models.CASCADE, verbose_name='Олимпиада'
    )
    minRezult = models.IntegerField(
        verbose_name='Минимальный резултат по оценке softskill для '
        'предположительного успеха в олимпиаде',
        default=0
    )


# Wagtails models
# ----------------


class Test(Page):
    template = "home/test_preview.html"

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, on_delete=models.SET_NULL,
        verbose_name="Изображение для страницы теста",
        related_name='+',
    )
    intro = RichTextField(verbose_name="Введение", blank=True)
    softSkill = models.ForeignKey(
        SoftSkill, on_delete=models.SET_NULL, verbose_name="Навык",
        blank=True, null=True
    )
    thank_you_text = RichTextField(
        verbose_name="Благодарственный текст", blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('softSkill'),
        FieldPanel('image'),
        FieldPanel('intro'),
        InlinePanel(
            'questions',
            label="Вопрос",
            help_text="Вопросы должны быть в порядке добавления. Поменять их местами не удастся."
        ),
        FieldPanel('thank_you_text'),
    ]

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"

    @property
    def count_scores(self) -> int:
        """
        Количество очков возможных для максимального набора за
        правильно решенные вопросы.

        :return: Максимальное количество очков
        """
        return self.questions.aggregate(sum=Sum('score'))['sum'] or 0


class Question(ClusterableModel):
    test = ParentalKey(Test, on_delete=models.CASCADE,
                       related_name='questions')
    question_text = RichTextField(verbose_name="Текст вопроса", blank=True)
    time_limit = models.PositiveIntegerField(
        verbose_name="Ограничение по времени (в секундах)", blank=True, null=True)
    score = models.PositiveIntegerField(
        verbose_name="Очки за правильный ответ", blank=True, null=True)

    panels = [
        FieldPanel(
            'question_text',
            help_text="Поддерживается использование markdown разметки. "
        ),
        FieldPanel('time_limit'),
        FieldPanel('score'),
        InlinePanel(
            'answers', label="Ответы",
            panels=[
                FieldPanel('answer_text'),
                FieldPanel('correct'),
            ],
            help_text="Для вопросов доступны различные варианты ответов:\n"
            "- Выбор одного варианта;\n"
            "- Выбор нескольких вариантов;\n"
            "- Поле для ввода (используйте одно поле ответа и перечислите варианты правильных ответов через запятую)",
        ),
    ]

    @property
    def count_answers(self) -> int:
        """
        Количество ответов на вопрос.

        :return: количество ответов на вопрос
        """
        return self.answers.count()

    @property
    def count_correct_answers(self) -> int:
        """
        Количество правильных ответов на вопрос.

        :return: количество правильных ответов на вопрос
        """
        return self.answers.filter(correct=True).count()

    @property
    def type_answer(self) -> str:
        """
        Тип ответа на вопрос.

        :return: тип ответа
        """
        count_answer = self.count_answers
        if count_answer == 1:
            return "input"
        correct_count = self.answers.filter(correct=True).count()
        if correct_count == 1:
            return "radio"
        return "checkbox"


class Answer(models.Model):
    question = ParentalKey(
        Question, on_delete=models.CASCADE, related_name='answers')
    answer_text = RichTextField(verbose_name="Ответ", blank=True)
    correct = models.BooleanField(
        verbose_name="Правильный ответ", default=False)


class SoftSkillUser(models.Model):
    """
    Модель для хранения информации о
    результате прохождения softskill-а пользователем.

    Fields:
        user - пользователь, проходивший тест
        softskill - тест softskill-а
        softSkillResult - результат прохождения теста
    """
    class Meta:
        verbose_name = "Softskill result"
        verbose_name_plural = "Softskill results"

    user = models.ForeignKey(
        StudentProfile, on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    softskill = models.ForeignKey(
        Test, on_delete=models.CASCADE,
        verbose_name='Softskill'
    )
    """
    TODO:
    Случается такое, что результаты тестирования имеют float-типы.
    Однако в рамках "ОЦЕНКИ ОЛИМПИАД" используется только целое число.
    Вопрос:
        Следует ли использовать float для данного поля?
        Или можно использовать int, приведя результат к целому числу?
            - Сокращение результата или округление в какую-то сторону
    """
    softSkillResult = models.IntegerField(
        verbose_name='Результат softskill',
        choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    )


class HomePage(Page):
    """
    Home page of the site.

    Contains a RichTextField for editing page content.
    """

    class Meta:
        verbose_name = "Главная страница"
        verbose_name_plural = "Главные страницы"

    body = RichTextField(blank=True, verbose_name="Контент страницы")
    content_panels = Page.content_panels + [
        FieldPanel("body", classname="full"),
    ]


# class VideoPage(Page):
#     video = EmbedBlock(
#         icon="media",
#         label="Видео",
#         help_text="Вставьте ссылку на видео",
#         verbose_name="Видео",
#     )
#     content_panels = Page.content_panels + [
#         FieldPanel("video", classname="full"),
#     ]

#     class Meta:
#         verbose_name = "Видео"
#         verbose_name_plural = "Видео"
