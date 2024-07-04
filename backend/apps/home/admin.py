from wagtail_modeladmin.options import (
    ModelAdmin, modeladmin_register, ModelAdminGroup
)

from apps.auth_app.models import (
    City,
)

from .models import (
    Lesson, Olimpiad, SoftSkill, SoftSkillTest
)

from .filters import (
    MultipleAdditionalLessonFilter,
    MultipleBaseLessonFilter,
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


class SoftSkillTestAdmin(ModelAdmin):
    model = SoftSkillTest
    menu_label = "Мягкие навыки"
    menu_icon = 'doc-full-inverse'
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('softSkill',)


class OlimpiadAdmin(ModelAdmin):
    model = Olimpiad
    menu_label = 'Олимпиады'
    menu_icon = 'doc-full-inverse'
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('name',  'difficultyLevel', 'difficultyLevelMinObr')
    list_filter = ('difficultyLevelMinObr', 'difficultyLevel',
                   MultipleBaseLessonFilter, MultipleAdditionalLessonFilter)
    list_export = ('name', 'link', 'difficultyLevel', 'difficultyLevelMinObr')
    search_fields = ('name', 'link')
    index_template_name = 'wagtailadmin/olimpiad/index.html'
    create_template_name = 'wagtailadmin/olimpiad/create.html'
    edit_template_name = 'wagtailadmin/olimpiad/edit.html'


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
        SoftSkillTestAdmin,
        OlimpiadAdmin,
        SoftSkillAdmin, LessonAdmin,
        CityAdmin,
    )


# Регистрация ModelAdmins
modeladmin_register(CustomGroupModelAdmin)
