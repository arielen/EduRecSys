import pandas as pd

from collections import defaultdict

from .models import (
    Olimpiad, BaseOlimpiadLesson, AdditionalOlimpiadLesson, OlimpiadSS,
    SoftSkill, Lesson
)


class Importer:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.df = None

    def import_data(self) -> None:
        df = pd.read_excel(
            self.file_path, sheet_name="Сводная оценка олимпиад", header=1)
        df = df[1:]
        self.df = df.fillna('')

    def create_olimpiads(self) -> None:
        olimpiadDict = {
            'name': 'Название олимпиады',
            'info': 'Описание олимпиады',
            'difficultyLevel': 'Уровень сложности олимпиады',
            'difficultyLevelMinObr': 'Уровень олимпиады согласно приказа Минобрнауки №823 от 28.08.2023',
        }
        softSkillDict = {
            'Креативность': 'Креативность (умение настандартно мыслить)',
            'Самоорганизация': 'Самоорганизация',
            'Критическое мышление': 'Критическое мышление',
            'Читательская грамотность': 'Читательская грамотность',
            'Логическое мышление': 'Логическое мышление',
            'Эмоциональный интеллект': 'Устойчивость к стрессу (умение работать в режиме высокой неопределенности)',
            'Память': 'Управление вниманием',
        }
        levelMinObrIdDict = defaultdict(int, {
            'Не является перечневой': 0,
            '1 уровень': 1,
            '2 уровень': 2,
            '3 уровень': 3,
        })

        def get_or_create_olimpiad(row) -> Olimpiad:
            difficultyLevel = row.get(olimpiadDict['difficultyLevel'], 0)
            difficultyLevelMinObr = levelMinObrIdDict[
                row.get(olimpiadDict['difficultyLevelMinObr'], 0)
            ]
            olimpiad, created = Olimpiad.objects.update_or_create(
                name=row[olimpiadDict['name']],
                defaults={
                    'info': row[olimpiadDict['info']],
                    'difficultyLevel': difficultyLevel,
                    'difficultyLevelMinObr': difficultyLevelMinObr,
                }
            )
            if created:
                print("Created: ", olimpiad)
            return olimpiad

        def create_or_update_softskills(olimpiad: Olimpiad, row) -> None:
            for key, value in softSkillDict.items():
                try:
                    softskill = SoftSkill.objects.get(name=key)
                    minRezult = row.get(value, 0)
                    OlimpiadSS.objects.update_or_create(
                        olimpiad=olimpiad,
                        ss=softskill,
                        defaults={'minRezult': minRezult}
                    )
                except SoftSkill.DoesNotExist:
                    print(f"SoftSkill {key} does not exist")

        def create_or_update_base_lessons(olimpiad: Olimpiad, row) -> None:
            baseOlimpiadLesson = {
                'lesson': 'Наименование базового школьного предмета',
                'minAvgMarkFor3Years': 'Мин. среднее значение ГОДОВЫХ оценок школьника по предмету за 3 прошедших учебных года, которое нужно, чтобы система могла порекомендовать олимпиаду школьнику',
                'interest': 'На сколько школьник должен быть НА ТЕКУЩИЙ МОМЕНТ заинтересован в предмете, по указанной шкале, чтобы система могла порекоменовать ему участие в рассматриваемой олимпиаде?',
                'minAvgRezult': 'Мин. средний показатель результатов участия в олимпиадах различных уровней по предмету на текущий момент, который необходим, чтобы система могла рекомендовать олимпиаду'
            }
            lesson = Lesson.objects.filter(
                lessonName=row[baseOlimpiadLesson['lesson']]).first()
            if lesson:
                base_olimpiad_lesson, created_base_olimpiad_lesson = BaseOlimpiadLesson.objects.update_or_create(
                    lesson=lesson,
                    olimpiad=olimpiad,
                    defaults={
                        'minAvgMarkFor3Years': row.get(baseOlimpiadLesson['minAvgMarkFor3Years'], 0),
                        'interest': row.get(baseOlimpiadLesson['interest'], 0),
                        'minAvgRezult': row.get(baseOlimpiadLesson['minAvgRezult'], 0)
                    }
                )
                if created_base_olimpiad_lesson:
                    print(f"Created: {base_olimpiad_lesson}")
            else:
                print(f"Lesson not found: {row[baseOlimpiadLesson['lesson']]}")

        def create_or_update_additional_lessons(olimpiad, row):
            additionalOlimpiadLesson = {
                'lesson': 'Наименование школьного предмета',
                'minAvgMarkFor3Years': 'Мин. среднее значение ГОДОВЫХ оценок школьника по предмету за 3 прошедших учебных года, которое нужно, чтобы система могла порекомендовать олимпиаду школьнику',
                'interest': 'На сколько школьник должен быть НА ТЕКУЩИЙ МОМЕНТ заинтересован в предмете, по указанной шкале, чтобы система могла порекоменовать ему участие в рассматриваемой олимпиаде?',
                'minAvgRezult': 'Мин. средний показатель результатов участия в олимпиадах и конкурсах по предмету на текущий момент, который необходим, чтобы рекомендовать олимпиаду'
            }
            added_separator = {
                'lesson': ['', '.1', '.2'],
                'minAvgMarkFor3Years': ['.1', '.2', '.3'],
                'interest': ['.1', '.2', '.3'],
                'minAvgRezult': ['', '.1', '.2']
            }
            for index in range(3):
                lesson_key = additionalOlimpiadLesson['lesson'] + \
                    added_separator['lesson'][index]
                minAvgMarkFor3Years_key = additionalOlimpiadLesson['minAvgMarkFor3Years'] + \
                    added_separator['minAvgMarkFor3Years'][index]
                interest_key = additionalOlimpiadLesson['interest'] + \
                    added_separator['interest'][index]
                minAvgRezult_key = additionalOlimpiadLesson['minAvgRezult'] + \
                    added_separator['minAvgRezult'][index]

                if row.get(lesson_key, '') != 'НЕ ПРИМЕНИМО':
                    lesson = Lesson.objects.filter(
                        lessonName=row[lesson_key]
                    ).first()
                    if lesson:
                        additional_olimpiad_lesson, created_additional_olimpiad_lesson = AdditionalOlimpiadLesson.objects.update_or_create(
                            lesson=lesson,
                            olimpiad=olimpiad,
                            defaults={
                                'minAvgMarkFor3Years': row.get(minAvgMarkFor3Years_key, 0),
                                'interest': row.get(interest_key, 0),
                                'minAvgRezult': row.get(minAvgRezult_key, 0)
                            }
                        )
                        if created_additional_olimpiad_lesson:
                            print(f"Created: {additional_olimpiad_lesson}")
                    else:
                        print(f"Lesson not found: {row[lesson_key]}")

        df = self.df.fillna('')
        for _, row in df.iterrows():
            olimpiad = get_or_create_olimpiad(row)
            create_or_update_softskills(olimpiad, row)
            create_or_update_base_lessons(olimpiad, row)
            create_or_update_additional_lessons(olimpiad, row)
