from django.conf import settings
from django.core.mail import send_mail

from .models import User


def send_confirmation_code(username, email):
    sender = settings.EMAIL_HOST_USER
    subject = 'Your account confirmation code'
    user_obj = User.objects.get(username=username)
    confirmation_code = user_obj.code_gen()
    message = f'Your confirmation code is {confirmation_code} '
    send_mail(subject, message, sender, [email])
    user_obj.confirmation_code = confirmation_code
    user_obj.save()
