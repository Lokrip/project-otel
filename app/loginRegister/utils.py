from django.contrib.auth.base_user import AbstractBaseUser  # Импортируем генератор токенов для сброса пароля
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six # Импортируем библиотеку six для совместимости кода между Python 2 и 3

class TokenGenerator(PasswordResetTokenGenerator): # Создаем класс генератора токенов
    def _make_hash_value(self, user: AbstractBaseUser, timestamp: int) -> str: # Определяем, как создается хеш-значение
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )

account_activation_token = TokenGenerator()