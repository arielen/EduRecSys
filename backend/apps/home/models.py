from django.db import models
from django.db.models import Sum
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


def student_profile_photo(instance: 'StudentProfile', filename: str) -> str:
    return "student_profile/{0}/{1}".format(instance.user.username, filename)


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
    photo = models.ImageField(
        upload_to=student_profile_photo, verbose_name='Фото',
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
        choices=[(1, '1 (???)'), (2, '2 (неуд.)'), (3, '3 (удовл.)'),
                 (4, '4 (хор.)'), (5, '5 (отл.)')]
    )

    def __str__(self) -> str:
        return f"{self.user} {self.lesson} {self.mark}"


class Olimpiad(ClusterableModel):
    """
    Модель для хранения информации о конкретной олимпиаде.

    Fields:
        name: Название олимпиады.
        link: Ссылка на олимпиаду.
    """
    class Meta:
        verbose_name = "Олимпиада"
        verbose_name_plural = "Олимпиады"

    name = models.CharField(verbose_name='Название олимпиады')
    link = models.URLField(verbose_name='Ссылка на олимпиаду')
    info = RichTextField(verbose_name='Описание олимпиады',
                         blank=True, null=True)
    difficultyLevel = models.IntegerField(
        verbose_name='Уровень сложности олимпиады',
        choices=[(i, i) for i in range(1, 11)],
        blank=True, null=True
    )
    difficultyLevelMinObr = models.IntegerField(
        verbose_name='Уровень олимпиады согласно приказа Минобрнауки №823 от 28.08.2023',
        choices=[
            (0, 'Не является перечневой'),
            (1, '1 уровень'),
            (2, '2 уровень'),
            (3, '3 уровень'),
        ],
        blank=True, null=True
    )

    def __str__(self) -> str:
        return self.name

    panels = [
        FieldPanel('name'),
        FieldPanel('link'),
        FieldPanel('info'),
        FieldPanel('difficultyLevel'),
        FieldPanel('difficultyLevelMinObr'),
        InlinePanel(
            'baseolimpiadlesson', label="Базовый школьный предмет",
            panels=[
                FieldPanel('lesson'),
                FieldPanel('minAvgMarkFor3Years'),
                FieldPanel('interest'),
                FieldPanel('minAvgRezult'),
            ],
            max_num=1
        ),
        InlinePanel(
            'additionalolimpiadlesson', label="Дополнительный школьный предмет",
            panels=[
                FieldPanel('lesson'),
                FieldPanel('minAvgMarkFor3Years'),
                FieldPanel('interest'),
                FieldPanel('minAvgRezult'),
            ],
            max_num=3
        ),
        InlinePanel(
            'olimpiadsoftskill', label="SoftSkills необходимые для рекомендации",
            panels=[
                FieldPanel('ss'),
                FieldPanel('minRezult'),
            ],
            max_num=7
        ),
    ]


class BaseOlimpiadLesson(models.Model):
    class Meta:
        verbose_name = "Базовый школьный предмет"
        verbose_name_plural = "Базовые школьные предметы"

    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, verbose_name='Базовый школьный предмет'
    )
    olimpiad = ParentalKey(
        Olimpiad, on_delete=models.CASCADE,
        related_name='baseolimpiadlesson'
    )
    minAvgMarkFor3Years = models.IntegerField(
        verbose_name='Мин. среднее значение ГОДОВЫХ оценок школьника по предмету за 3 прошедших учебных года',
        choices=[(i, i) for i in range(1, 6)],
    )
    interest = models.IntegerField(
        verbose_name='На сколько школьник должен быть НА ТЕКУЩИЙ МОМЕНТ заинтересован в предмете, по указанной шкале',
        choices=[
            (1, "1 - предмет совершенно не интересен"),
            (2, "2 - нейтральное отношение"),
            (3, "3 - предмет интересен"),
            (4, "4 - предмет интересен, изучаю дополнительно"),
            (5, "5 - предмет интересен, участвую в олимпиадах, конкурсах и др."),
            (0, "0 - НЕ ПРИМЕНИМО"),
        ],
    )
    minAvgRezult = models.IntegerField(
        verbose_name="Мин. средний показатель результатов участия в олимпиадах различных уровней по предмету на текущий момент, который необходим, чтобы система могла рекомендовать олимпиаду",
        choices=[
            (1, "1 - не участвовал в олимпиадах и конкурсах"),
            (2, "2 - участвовал в школьных и городских, но не побеждал "),
            (3, "3 - побеждал в школьных и городских / участвовал в региональных"),
            (4, "4 - побеждал в региональных / участвовал в федеральных конкурсах, в том числе Перечневых Олимпиадах"),
            (5, "5 - побеждал в федеральных конкурсах или Перечневых Олимпиадах"),
            (0, "0 - НЕ ПРИМЕНИМО")
        ],
    )


class AdditionalOlimpiadLesson(models.Model):
    class Meta:
        verbose_name = "Дополнительный школьный предмет"
        verbose_name_plural = "Дополнительные школьные предметы"

    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, verbose_name='Дополнительный школьный предмет'
    )
    olimpiad = ParentalKey(
        Olimpiad, on_delete=models.CASCADE,
        related_name='additionalolimpiadlesson'
    )
    minAvgMarkFor3Years = models.IntegerField(
        verbose_name='Мин. среднее значение ГОДОВЫХ оценок школьника по предмету за 3 прошедших учебных года',
        choices=[(i, i) for i in range(1, 6)],
    )
    interest = models.IntegerField(
        verbose_name='На сколько школьник должен быть НА ТЕКУЩИЙ МОМЕНТ заинтересован в предмете, по указанной шкале',
        choices=[
            (1, "1 - предмет совершенно не интересен"),
            (2, "2 - нейтральное отношение"),
            (3, "3 - предмет интересен"),
            (4, "4 - предмет интересен, изучаю дополнительно"),
            (5, "5 - предмет интересен, участвую в олимпиадах, конкурсах и др."),
            (0, "0 - НЕ ПРИМЕНИМО"),
        ],
    )
    minAvgRezult = models.IntegerField(
        verbose_name="Мин. средний показатель результатов участия в олимпиадах различных уровней по предмету на текущий момент, который необходим, чтобы система могла рекомендовать олимпиаду",
        choices=[
            (1, "1 - не участвовал в олимпиадах и конкурсах"),
            (2, "2 - участвовал в школьных и городских, но не побеждал "),
            (3, "3 - побеждал в школьных и городских / участвовал в региональных"),
            (4, "4 - побеждал в региональных / участвовал в федеральных конкурсах, в том числе Перечневых Олимпиадах"),
            (5, "5 - побеждал в федеральных конкурсах или Перечневых Олимпиадах"),
            (0, "0 - НЕ ПРИМЕНИМО")
        ],
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
    olimpiad = ParentalKey(
        Olimpiad, on_delete=models.CASCADE, verbose_name='Олимпиада',
        related_name='olimpiadsoftskill'
    )
    minRezult = models.IntegerField(
        verbose_name='Минимальный резултат по оценке softskill для '
        'предположительного успеха в олимпиаде',
        choices=[
            (0, "0 - навык отсутствует"),
            (1, "1 - низкий"),
            (2, "2 - ниже среднего"),
            (3, "3 - средний"),
            (4, "4 - выше среднего"),
            (5, "5 - высокий")
        ]
    )


# Wagtails models
# ----------------


class SoftSkillTest(ClusterableModel):
    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True, on_delete=models.SET_NULL,
        verbose_name="Изображение для страницы теста",
        related_name='+',
    )
    intro = RichTextField(verbose_name="Введение", blank=True)
    softSkill = models.ForeignKey(
        SoftSkill, on_delete=models.SET_NULL, verbose_name="Навык",
        blank=True, null=True
    )

    panels = [
        FieldPanel('softSkill'),
        FieldPanel('image'),
        FieldPanel('intro'),
        InlinePanel(
            'questions',
            label="Вопрос",
            help_text="Вопросы должны быть в порядке добавления. Поменять их местами не удастся."
        ),
    ]

    def __str__(self) -> str:
        return self.softSkill.name

    @property
    def count_scores(self) -> int:
        """
        Количество очков возможных для максимального набора за
        правильно решенные вопросы.

        :return: Максимальное количество очков
        """
        return self.questions.aggregate(sum=Sum('score'))['sum'] or 0

    @property
    def get_time_limits(self) -> list[int]:
        """
        Список ограничений по времени для каждого вопроса.

        :return: Список ограничений по времени
        """
        return [
            q.time_limit if q.time_limit else 0
            for q in self.questions.all()
        ]


class Question(ClusterableModel):
    test = ParentalKey(SoftSkillTest, on_delete=models.CASCADE,
                       related_name='questions')
    question_text = RichTextField(verbose_name="Текст вопроса", blank=True)
    time_limit = models.PositiveIntegerField(
        verbose_name="Ограничение по времени (в секундах)", blank=True, null=True)
    score = models.PositiveIntegerField(
        verbose_name="Очки за правильный ответ", blank=True, null=True)
    additional_text = RichTextField(
        verbose_name="Дополнительный текст", blank=True, null=True
    )

    panels = [
        FieldPanel(
            'question_text',
            help_text="Поддерживается использование markdown разметки. "
        ),
        FieldPanel('time_limit'),
        FieldPanel('score'),
        FieldPanel(
            'additional_text',
            help_text="Используйте как дополнение, в случае если есть лимит "
            "по времени, то он будет показываться как вспомогательный"
        ),
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

    @ property
    def count_answers(self) -> int:
        """
        Количество ответов на вопрос.

        :return: количество ответов на вопрос
        """
        return self.answers.count()

    @ property
    def count_correct_answers(self) -> int:
        """
        Количество правильных ответов на вопрос.

        :return: количество правильных ответов на вопрос
        """
        return self.answers.filter(correct=True).count()

    @ property
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
        SoftSkillTest, on_delete=models.CASCADE,
        verbose_name='Softskill'
    )
    softSkillResult = models.IntegerField(
        verbose_name='Результат softskill',
        choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    )

    @property
    def percent(self) -> int:
        return int(self.softSkillResult / self.softskill.count_scores * 100)

    @property
    def progress_status(self) -> str:
        if self.percent >= 66:
            return "success"
        elif self.percent >= 33:
            return "warning"
        return "danger"


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
