from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

from home.models import (
    StudentProfile, City, School
)


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        label='Адрес электронной почты',
        help_text='Обязательное поле. Укажите действующий адрес электронной почты.',
        max_length=254, required=True,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Укажите действующий адрес электронной почты'
            }
        ),
    )
    first_name = forms.CharField(
        max_length=30, required=True,
        help_text='Обязательное поле.',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Укажите ваше имя'
            }
        ),
    )
    last_name = forms.CharField(
        max_length=150, required=True,
        help_text='Обязательное поле.',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Укажите вашу фамилию'
            }
        ),
    )
    city = forms.ModelChoiceField(
        empty_label="Выберите город",
        queryset=City.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    school = forms.ModelChoiceField(
        empty_label="Выберите школу",
        queryset=School.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    classNumber = forms.ChoiceField(
        help_text='Выберите класс',
        choices=[(i, i) for i in range(1, 12)],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    sex = forms.ChoiceField(
        label='Пол',
        choices=[(True, 'Мужской'), (False, 'Женский')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    startYear = forms.DateField(
        label='Год начала обучения',
        help_text='Выберите год начала обучения',
        required=False,
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Укажите год начала обучения'
            }
        ),
    )
    password1 = forms.CharField(
        label='Пароль',
        help_text='Обязательное поле. Введите пароль.',
        strip=True, required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    password2 = forms.CharField(
        label='Подтвердите пароль',
        help_text='Обязательное поле. Повторите ввод пароля.',
        strip=True, required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = User
        fields = (
            # 'username',
            'first_name', 'last_name', 'email',
            'password1', 'password2',
            'city', 'school', 'classNumber', 'sex', 'startYear'
        )

    def clean_password2(self) -> str:
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                "Пароли не совпадают!"
            )
        return password2

    def clean_email(self) -> str:
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Пользователь с таким адресом электронной почты уже зарегистрирован"
            )
        return email

    def generate_unique_username(self) -> str:
        while True:
            # Генерируем случайное имя пользователя
            # Можно изменить длину по желанию
            username = f"user-{get_random_string(length=8)}"
            # Проверяем, не существует ли уже такого имени пользователя
            if not User.objects.filter(username=username).exists():
                return username

    def save(self, commit: bool = True) -> User:
        username = self.generate_unique_username()
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=username,
                email=self.cleaned_data['email'],
                password=self.cleaned_data['password1'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name']
            )
            StudentProfile.objects.create(
                user=user,
                city=self.cleaned_data['city'],
                school=self.cleaned_data['school'],
                classNumber=self.cleaned_data['classNumber'],
                sex=self.cleaned_data['sex'],
                startYear=self.cleaned_data['startYear']
            )
        self.cleaned_data["username"] = user.username
        if commit:
            user.save()
        return user


class ProfileEditForm(UserChangeForm):
    about = forms.CharField(
        label='О себе',
        required=False,
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'rows': 5}
        )
    )
    first_name = forms.CharField(
        label='Имя',
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    last_name = forms.CharField(
        label='Фамилия',
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    city = forms.ModelChoiceField(
        empty_label="Выберите город",
        queryset=City.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    school = forms.ModelChoiceField(
        empty_label="Выберите школу",
        queryset=School.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    classNumber = forms.ChoiceField(
        help_text='Выберите класс',
        choices=[(i, i) for i in range(1, 12)],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    sex = forms.ChoiceField(
        label='Пол',
        choices=[(True, 'Мужской'), (False, 'Женский')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    startYear = forms.DateField(
        label='Год начала обучения',
        help_text='Выберите год начала обучения',
        required=False,
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Укажите год начала обучения'
            }
        ),
    )
    photo = forms.ImageField(
        label='Фото',
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = StudentProfile
        fields = (
            'first_name', 'last_name',
            'about',
            'city', 'school', 'classNumber', 'sex', 'startYear', 'photo'
        )

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        user = kwargs['instance'].user
        self.fields['first_name'].initial = user.first_name
        self.fields['last_name'].initial = user.last_name

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        try:
            context['profile'] = StudentProfile.objects.get(user=user)
        except StudentProfile.DoesNotExist:
            context['profile'] = None
        return context
