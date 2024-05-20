import pandas as pd
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
            # TODO: уточнить по нижним критериям
            'Эмоциональный интеллект': 'Устойчивость к стрессу (умение работать в режиме высокой неопределенности)',
            'Память': 'Управление вниманием',
        }
        levelMinObrIdDict = {
            '': 0,
            'Не является перечневой': 0,
            '1 уровень': 1,
            '2 уровень': 2,
            '3 уровень': 3,
        }
        df = self.df
        for index, row in df.iterrows():
            difficultyLevel = row[olimpiadDict['difficultyLevel']
                                  ] if row[olimpiadDict['difficultyLevel']] else 0
            difficultyLevelMinObr = levelMinObrIdDict.get(
                row[olimpiadDict['difficultyLevelMinObr']])
            olimpiad, created = Olimpiad.objects.get_or_create(
                name=row[olimpiadDict['name']],
                info=row[olimpiadDict['info']],
                difficultyLevel=difficultyLevel,
                difficultyLevelMinObr=difficultyLevelMinObr,
            )
            if created:
                print("Created: ", olimpiad)
                olimpiad.save()
            for key, value in softSkillDict.items():
                softskill = SoftSkill.objects.get(name=key)
                if softskill:
                    minRezult = row[value] if row[value] else 0
                    olimpiad_ss, created_olimpiad_ss = OlimpiadSS.objects.get_or_create(
                        olimpiad=olimpiad,
                        ss=softskill,
                        minRezult=minRezult
                    )
                    if created_olimpiad_ss:
                        olimpiad_ss.save()
                    elif olimpiad_ss.minRezult != minRezult:
                        olimpiad_ss.minRezult = minRezult
                        olimpiad_ss.save()

            # Заполняем базовые школьные предметы
            baseOlimpiadLesson = {
                'lesson': 'Наименование базового школьного предмета',
                'minAvgMarkFor3Years': 'Мин. среднее значение ГОДОВЫХ оценок школьника по предмету за 3 прошедших учебных года, которое нужно, чтобы система могла порекомендовать олимпиаду школьнику',
                'interest': 'На сколько школьник должен быть НА ТЕКУЩИЙ МОМЕНТ заинтересован в предмете, по указанной шкале, чтобы система могла порекоменовать ему участие в рассматриваемой олимпиаде?',
                'minAvgRezult': 'Мин. средний показатель результатов участия в олимпиадах различных уровней по предмету на текущий момент, который необходим, чтобы система могла рекомендовать олимпиаду'
            }
            lesson = Lesson.objects.get(
                lessonName=row[baseOlimpiadLesson['lesson']])
            if lesson:
                minAvgMarkFor3Years = row[baseOlimpiadLesson['minAvgMarkFor3Years']
                                          ] if row[baseOlimpiadLesson['minAvgMarkFor3Years']] else 0
                interest = row[baseOlimpiadLesson['interest']
                               ] if row[baseOlimpiadLesson['interest']] else 0
                minAvgRezult = row[baseOlimpiadLesson['minAvgRezult']
                                   ] if row[baseOlimpiadLesson['minAvgRezult']] else 0
                base_olimpiad_lesson, created_base_olimpiad_lesson = BaseOlimpiadLesson.objects.get_or_create(
                    lesson=lesson,
                    olimpiad=olimpiad,
                    minAvgMarkFor3Years=minAvgMarkFor3Years,
                    interest=interest,
                    minAvgRezult=minAvgRezult
                )
                if created_base_olimpiad_lesson:
                    base_olimpiad_lesson.save()
                elif base_olimpiad_lesson.minAvgMarkFor3Years != minAvgMarkFor3Years \
                    or base_olimpiad_lesson.interest != interest \
                        or base_olimpiad_lesson.minAvgRezult != minAvgRezult:
                    base_olimpiad_lesson.minAvgMarkFor3Years = minAvgMarkFor3Years
                    base_olimpiad_lesson.interest = interest
                    base_olimpiad_lesson.minAvgRezult = minAvgRezult
                    base_olimpiad_lesson.save()
            else:
                print("Lesson not found: ", row[baseOlimpiadLesson['lesson']])

            additionalOlimpiadLesson = {
                # добавляется ".1", ".2", ".3"
                'lesson': 'Наименование школьного предмета',
                # добавляется ".1", ".2", ".3"
                'minAvgMarkFor3Years': 'Мин. среднее значение ГОДОВЫХ оценок школьника по предмету за 3 прошедших учебных года, которое нужно, чтобы система могла порекомендовать олимпиаду школьнику',
                # добавляется ".1", ".2", ".3"
                'interest': 'На сколько школьник должен быть НА ТЕКУЩИЙ МОМЕНТ заинтересован в предмете, по указанной шкале, чтобы система могла порекоменовать ему участие в рассматриваемой олимпиаде?',

                # первая идет без точки, последующие ".1", ".2"
                'minAvgRezult': 'Мин. средний показатель результатов участия в олимпиадах и конкурсах по предмету на текущий момент, который необходим, чтобы рекомендовать олимпиаду'
            }
            added_separator = {
                'lesson': ['', '.1', '.2'],
                'minAvgMarkFor3Years': ['.1', '.2', '.3'],
                'interest': ['.1', '.2', '.3'],
                'minAvgRezult': ['', '.1', '.2']
            }
            # TODO: add separator
            for index in range(0, 3):
                lesson = additionalOlimpiadLesson['lesson'] + \
                    added_separator['lesson'][index]
                minAvgMarkFor3Years = additionalOlimpiadLesson['minAvgMarkFor3Years'] + \
                    added_separator['minAvgMarkFor3Years'][index]
                interest = additionalOlimpiadLesson['interest'] + \
                    added_separator['interest'][index]
                minAvgRezult = additionalOlimpiadLesson['minAvgRezult'] + \
                    added_separator['minAvgRezult'][index]

                if row[lesson] != 'НЕ ПРИМЕНИМО':
                    lesson = Lesson.objects.get(lessonName=row[lesson])
                    if lesson:
                        additional_olimpiad_lesson, created_additional_olimpiad_lesson = AdditionalOlimpiadLesson.objects.get_or_create(
                            lesson=lesson,
                            olimpiad=olimpiad,
                            minAvgMarkFor3Years=row[minAvgMarkFor3Years],
                            interest=row[interest],
                            minAvgRezult=row[minAvgRezult]
                        )
                        if created_additional_olimpiad_lesson:
                            additional_olimpiad_lesson.save()
                        elif additional_olimpiad_lesson.minAvgMarkFor3Years != row[minAvgMarkFor3Years] \
                            or additional_olimpiad_lesson.interest != row[interest] \
                                or additional_olimpiad_lesson.minAvgRezult != row[minAvgRezult]:
                            additional_olimpiad_lesson.minAvgMarkFor3Years = row[minAvgMarkFor3Years]
                            additional_olimpiad_lesson.interest = row[interest]
                            additional_olimpiad_lesson.minAvgRezult = row[minAvgRezult]
                            additional_olimpiad_lesson.save()
