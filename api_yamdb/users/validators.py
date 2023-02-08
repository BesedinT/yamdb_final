from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError


class UsernameRegexValidator(UnicodeUsernameValidator):
    regex = r'^[\w.@+-]+\z'
    flags = 0


def me_username(value):
    if value == 'me':
        raise ValidationError(
            'Недопустимый username "me" '
        )
