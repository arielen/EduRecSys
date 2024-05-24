from django.contrib.admin import SimpleListFilter
from django.db.models import Q

from .models import BaseOlimpiadLesson, AdditionalOlimpiadLesson


class MultipleBaseLessonFilter(SimpleListFilter):
    title = 'Основной предмет'
    parameter_name = 'base_lesson'

    def lookups(self, request, model_admin):
        lessons = BaseOlimpiadLesson.objects.values_list(
            'lesson__lessonName', flat=True).distinct()
        return [(lesson, lesson) for lesson in lessons]

    def queryset(self, request, queryset):
        if self.value():
            values = self.value().split(',')
            query = Q()
            for value in values:
                query |= Q(baseolimpiadlesson__lesson__lessonName=value)
            return queryset.filter(query).distinct()
        return queryset


class MultipleAdditionalLessonFilter(SimpleListFilter):
    title = 'Дополнительный предмет'
    parameter_name = 'additional_lessons'

    def lookups(self, request, model_admin):
        lessons = AdditionalOlimpiadLesson.objects.values_list(
            'lesson__lessonName', flat=True).distinct()
        return [(lesson, lesson) for lesson in lessons]

    def queryset(self, request, queryset):
        if self.value():
            values = self.value().split(',')
            query = Q()
            for value in values:
                query |= Q(additionalolimpiadlesson__lesson__lessonName=value)
            return queryset.filter(query).distinct()
        return queryset
