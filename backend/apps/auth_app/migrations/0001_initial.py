# Generated by Django 5.0.8 on 2024-08-23 12:02

import apps.auth_app.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cityName', models.CharField(max_length=255, verbose_name='Название города')),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'Города',
            },
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schoolName', models.CharField(max_length=50, verbose_name='Наименование школы')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth_app.city', verbose_name='Город')),
            ],
            options={
                'verbose_name': 'Школа',
                'verbose_name_plural': 'Школы',
            },
        ),
        migrations.CreateModel(
            name='StudentProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about', models.TextField(blank=True, null=True, verbose_name='О себе')),
                ('classNumber', models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11)], null=True, verbose_name='Номер класса')),
                ('sex', models.BooleanField(choices=[(True, 'Мужской'), (False, 'Женский')], default=True, verbose_name='Пол')),
                ('SNILS', models.CharField(blank=True, max_length=14, null=True, unique=True, verbose_name='СНИЛС')),
                ('startYear', models.IntegerField(blank=True, null=True, validators=[apps.auth_app.models.validate_start_year], verbose_name='Год начала обучения')),
                ('photo', models.ImageField(blank=True, null=True, upload_to=apps.auth_app.models.student_profile_photo, verbose_name='Фото')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth_app.city', verbose_name='Город')),
                ('school', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth_app.school', verbose_name='Школа')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
    ]
