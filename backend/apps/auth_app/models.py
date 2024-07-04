from django.db import models
from django.contrib.auth.models import User


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
    # lesson = models.ForeignKey(
    #     Lesson, on_delete=models.CASCADE, verbose_name='Урок',
    #     blank=True, null=True
    # )
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
