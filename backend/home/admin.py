from wagtail_modeladmin.options import (
    ModelAdmin, modeladmin_register, ModelAdminGroup
)

from .models import (
    City, Lesson, Olimpiad, SoftSkill
)


class SoftSkillAdmin(ModelAdmin):
    model = SoftSkill
    menu_label = "Навыки"
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('name',)
    search_fields = ('name',)


class LessonAdmin(ModelAdmin):
    model = Lesson
    menu_label = 'Дисциплины'  # название для меню
    # menu_icon = 'book'  # иконка из набора иконок Wagtail
    menu_order = 201  # порядок в меню
    add_to_settings_menu = False  # не добавлять в меню настроек
    exclude_from_explorer = False  # не исключать из исследователя сайта
    list_display = ('lessonName',)
    search_fields = ('lessonName',)


class OlimpiadAdmin(ModelAdmin):
    model = Olimpiad
    menu_label = 'Олимпиады'
    # menu_icon = 'group'
    menu_order = 202
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('name', 'link',)
    search_fields = ('name', 'link')


class CityAdmin(ModelAdmin):
    model = City
    menu_label = "Города"
    menu_order = 203
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('cityName',)
    search_fields = ('cityName',)


class CustomGroupModelAdmin(ModelAdminGroup):
    menu_label = 'Добавление данных'
    menu_order = 200
    items = (SoftSkillAdmin, LessonAdmin, OlimpiadAdmin, CityAdmin)


# Регистрация ModelAdmins
modeladmin_register(CustomGroupModelAdmin)
