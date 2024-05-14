from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend, UserModel
from django.core.exceptions import MultipleObjectsReturned
from django.db.models import Q


class EmailBackend(ModelBackend):
    """
    Аутентификация по электронной почте.

    Позволяет аутентифицироваться с помощью электронной почты или
    номера телефона пользователя (или любого другого уникального поля).
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Аутентифицировать пользователя по email-адресу.

        Если email-адрес не уникален, возвращается первый пользователь,
        соответствующий email-адресу.

        Возвращает None, если пользователь не найден.
        """
        try:
            user = UserModel.objects.get(
                Q(username__iexact=username) | Q(email__iexact=username))

        except UserModel.DoesNotExist:
            # Запустить стандартный хэшер паролей один раз,
            # чтобы уменьшить разницу во времени между существующим и
            # несуществующим пользователем (#20760)
            UserModel().set_password(password)
        except MultipleObjectsReturned:
            return User.objects.filter(email=username).order_by('id').first()
        else:
            if user.check_password(password) and \
                    self.user_can_authenticate(user):
                return user

    def get_user(self, user_id):
        """
        Получить пользователя по его id.

        Возвращает None, если пользователь не найден.
        """
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

        return user if self.user_can_authenticate(user) else None
