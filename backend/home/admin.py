import csv
from django.http import HttpRequest, HttpResponse
from django.db.models.options import Options
from django.db.models import QuerySet
from wagtail_modeladmin.options import (
    ModelAdmin, modeladmin_register, ModelAdminGroup
)

from .models import (
    City, Lesson, Olimpiad, SoftSkill,
)


class SoftSkillAdmin(ModelAdmin):
    model = SoftSkill
    menu_label = "Навыки"
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('name',)
    search_fields = ('name',)


class LessonAdmin(ModelAdmin):
    model = Lesson
    menu_label = 'Дисциплины'  # название для меню
    add_to_settings_menu = False  # не добавлять в меню настроек
    exclude_from_explorer = False  # не исключать из исследователя сайта
    list_display = ('lessonName',)
    search_fields = ('lessonName',)


class OlimpiadAdmin(ModelAdmin):
    model = Olimpiad
    menu_label = 'Олимпиады'
    menu_icon = 'doc-full-inverse'
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('name',  'difficultyLevel',
                    'difficultyLevelMinObr')
    search_fields = ('name', 'link')
    list_export = ('name', 'link', 'difficultyLevel', 'difficultyLevelMinObr')
    index_template_name = 'wagtailadmin/olimpiad/index.html'


class CityAdmin(ModelAdmin):
    model = City
    menu_label = "Города"
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('cityName',)
    search_fields = ('cityName',)


class CustomGroupModelAdmin(ModelAdminGroup):
    menu_label = 'Добавление данных'
    menu_order = 200
    items = (
        OlimpiadAdmin,
        SoftSkillAdmin, LessonAdmin,
        CityAdmin,
    )


# Регистрация ModelAdmins
modeladmin_register(CustomGroupModelAdmin)
