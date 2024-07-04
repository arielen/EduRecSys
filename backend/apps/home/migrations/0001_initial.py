# Generated by Django 5.0.6 on 2024-07-04 12:12

import apps.home.models
import django.db.models.deletion
import modelcluster.fields
import wagtail.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0091_remove_revision_submitted_for_moderation'),
        ('wagtailimages', '0025_alter_image_file_alter_rendition_file'),
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
            name='HomePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('body', wagtail.fields.RichTextField(blank=True, verbose_name='Контент страницы')),
            ],
            options={
                'verbose_name': 'Главная страница',
                'verbose_name_plural': 'Главные страницы',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lessonName', models.CharField(max_length=50, unique=True, verbose_name='Наименование дисциплины')),
            ],
            options={
                'verbose_name': 'Дисциплина',
                'verbose_name_plural': 'Дисциплины',
            },
        ),
        migrations.CreateModel(
            name='Olimpiad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(verbose_name='Название олимпиады')),
                ('link', models.URLField(verbose_name='Ссылка на олимпиаду')),
                ('info', wagtail.fields.RichTextField(blank=True, null=True, verbose_name='Описание олимпиады')),
                ('difficultyLevel', models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], null=True, verbose_name='Уровень сложности олимпиады')),
                ('difficultyLevelMinObr', models.IntegerField(blank=True, choices=[(0, 'Не является перечневой'), (1, '1 уровень'), (2, '2 уровень'), (3, '3 уровень')], null=True, verbose_name='Уровень олимпиады согласно приказа Минобрнауки №823 от 28.08.2023')),
            ],
            options={
                'verbose_name': 'Олимпиада',
                'verbose_name_plural': 'Олимпиады',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', wagtail.fields.RichTextField(blank=True, verbose_name='Текст вопроса')),
                ('time_limit', models.PositiveIntegerField(blank=True, null=True, verbose_name='Ограничение по времени (в секундах)')),
                ('score', models.PositiveIntegerField(blank=True, null=True, verbose_name='Очки за правильный ответ')),
                ('additional_text', wagtail.fields.RichTextField(blank=True, null=True, verbose_name='Дополнительный текст')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SoftSkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Наименование softskill-а')),
            ],
            options={
                'verbose_name': 'Softskill',
                'verbose_name_plural': 'Softskills',
            },
        ),
        migrations.CreateModel(
            name='BaseOlimpiadLesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minAvgMarkFor3Years', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], verbose_name='Мин. среднее значение ГОДОВЫХ оценок школьника по предмету за 3 прошедших учебных года')),
                ('interest', models.IntegerField(choices=[(1, '1 - предмет совершенно не интересен'), (2, '2 - нейтральное отношение'), (3, '3 - предмет интересен'), (4, '4 - предмет интересен, изучаю дополнительно'), (5, '5 - предмет интересен, участвую в олимпиадах, конкурсах и др.'), (0, '0 - НЕ ПРИМЕНИМО')], verbose_name='На сколько школьник должен быть НА ТЕКУЩИЙ МОМЕНТ заинтересован в предмете, по указанной шкале')),
                ('minAvgRezult', models.IntegerField(choices=[(1, '1 - не участвовал в олимпиадах и конкурсах'), (2, '2 - участвовал в школьных и городских, но не побеждал '), (3, '3 - побеждал в школьных и городских / участвовал в региональных'), (4, '4 - побеждал в региональных / участвовал в федеральных конкурсах, в том числе Перечневых Олимпиадах'), (5, '5 - побеждал в федеральных конкурсах или Перечневых Олимпиадах'), (0, '0 - НЕ ПРИМЕНИМО')], verbose_name='Мин. средний показатель результатов участия в олимпиадах различных уровней по предмету на текущий момент, который необходим, чтобы система могла рекомендовать олимпиаду')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.lesson', verbose_name='Базовый школьный предмет')),
                ('olimpiad', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='baseolimpiadlesson', to='home.olimpiad')),
            ],
            options={
                'verbose_name': 'Базовый школьный предмет',
                'verbose_name_plural': 'Базовые школьные предметы',
            },
        ),
        migrations.CreateModel(
            name='AdditionalOlimpiadLesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minAvgMarkFor3Years', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], verbose_name='Мин. среднее значение ГОДОВЫХ оценок школьника по предмету за 3 прошедших учебных года')),
                ('interest', models.IntegerField(choices=[(1, '1 - предмет совершенно не интересен'), (2, '2 - нейтральное отношение'), (3, '3 - предмет интересен'), (4, '4 - предмет интересен, изучаю дополнительно'), (5, '5 - предмет интересен, участвую в олимпиадах, конкурсах и др.'), (0, '0 - НЕ ПРИМЕНИМО')], verbose_name='На сколько школьник должен быть НА ТЕКУЩИЙ МОМЕНТ заинтересован в предмете, по указанной шкале')),
                ('minAvgRezult', models.IntegerField(choices=[(1, '1 - не участвовал в олимпиадах и конкурсах'), (2, '2 - участвовал в школьных и городских, но не побеждал '), (3, '3 - побеждал в школьных и городских / участвовал в региональных'), (4, '4 - побеждал в региональных / участвовал в федеральных конкурсах, в том числе Перечневых Олимпиадах'), (5, '5 - побеждал в федеральных конкурсах или Перечневых Олимпиадах'), (0, '0 - НЕ ПРИМЕНИМО')], verbose_name='Мин. средний показатель результатов участия в олимпиадах различных уровней по предмету на текущий момент, который необходим, чтобы система могла рекомендовать олимпиаду')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.lesson', verbose_name='Дополнительный школьный предмет')),
                ('olimpiad', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='additionalolimpiadlesson', to='home.olimpiad')),
            ],
            options={
                'verbose_name': 'Дополнительный школьный предмет',
                'verbose_name_plural': 'Дополнительные школьные предметы',
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', wagtail.fields.RichTextField(blank=True, verbose_name='Ответ')),
                ('correct', models.BooleanField(default=False, verbose_name='Правильный ответ')),
                ('question', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='home.question')),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schoolName', models.CharField(max_length=50, verbose_name='Наименование школы')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.city', verbose_name='Город')),
            ],
            options={
                'verbose_name': 'Школа',
                'verbose_name_plural': 'Школы',
            },
        ),
        migrations.CreateModel(
            name='OlimpiadSS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minRezult', models.IntegerField(choices=[(0, '0 - навык отсутствует'), (1, '1 - низкий'), (2, '2 - ниже среднего'), (3, '3 - средний'), (4, '4 - выше среднего'), (5, '5 - высокий')], verbose_name='Минимальный резултат по оценке softskill для предположительного успеха в олимпиаде')),
                ('olimpiad', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='olimpiadsoftskill', to='home.olimpiad', verbose_name='Олимпиада')),
                ('ss', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.softskill', verbose_name='Softskill')),
            ],
            options={
                'verbose_name': 'Olimpiad softskill',
                'verbose_name_plural': 'Olimpiad softskills',
            },
        ),
        migrations.CreateModel(
            name='SoftSkillTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intro', wagtail.fields.RichTextField(blank=True, verbose_name='Введение')),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image', verbose_name='Изображение для страницы теста')),
                ('softSkill', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.softskill', verbose_name='Навык')),
            ],
            options={
                'verbose_name': 'Тест',
                'verbose_name_plural': 'Тесты',
            },
        ),
        migrations.AddField(
            model_name='question',
            name='test',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='home.softskilltest'),
        ),
        migrations.CreateModel(
            name='StudentProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about', models.TextField(blank=True, null=True, verbose_name='О себе')),
                ('classNumber', models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11)], null=True, verbose_name='Номер класса')),
                ('sex', models.BooleanField(choices=[(True, 'Мужской'), (False, 'Женский')], default=True, verbose_name='Пол')),
                ('SNILS', models.CharField(blank=True, max_length=14, null=True, unique=True, verbose_name='СНИЛС')),
                ('startYear', models.DateField(blank=True, null=True, verbose_name='Год начала обучения')),
                ('photo', models.ImageField(blank=True, null=True, upload_to=apps.home.models.student_profile_photo, verbose_name='Фото')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.city', verbose_name='Город')),
                ('lesson', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.lesson', verbose_name='Урок')),
                ('school', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.school', verbose_name='Школа')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
        migrations.CreateModel(
            name='SoftSkillUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('softSkillResult', models.IntegerField(choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], verbose_name='Результат softskill')),
                ('softskill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.softskilltest', verbose_name='Softskill')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.studentprofile', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Softskill result',
                'verbose_name_plural': 'Softskill results',
            },
        ),
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.IntegerField(choices=[(1, '1 (???)'), (2, '2 (неуд.)'), (3, '3 (удовл.)'), (4, '4 (хор.)'), (5, '5 (отл.)')], verbose_name='Оценка')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.lesson', verbose_name='Урок')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.studentprofile', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Оценка',
                'verbose_name_plural': 'Оценки',
            },
        ),
        migrations.CreateModel(
            name='TestSS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.URLField(verbose_name='Ссылка на softskill')),
                ('softSkill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.softskill', verbose_name='Softskill')),
            ],
            options={
                'verbose_name': 'Test softskill',
                'verbose_name_plural': 'Test softskills',
            },
        ),
        migrations.CreateModel(
            name='TestSSUserResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('softSkillResult', models.IntegerField(verbose_name='Результат softskill')),
                ('softSkill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.testss', verbose_name='Test Softskill')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.studentprofile', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Test softskill result',
                'verbose_name_plural': 'Test softskill results',
            },
        ),
    ]
