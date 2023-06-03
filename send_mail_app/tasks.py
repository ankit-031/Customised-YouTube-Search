from django.contrib.auth import get_user_model

from celery import shared_task
from django.core.mail import send_mail
from django.core.serializers import serialize
from src import settings


@shared_task(bind=True)
def send_mail_func(self, user_email, token):
    # user = get_user_model().objects.all()
    print(user_email)
    print(token)
    # http://127.0.0.1:8000/verify/{auth_t}
    # for users in user:
    to_email = user_email
    mail_subject = f'Your accounts need to be verified'
    message = f'Hi, click on the link to verify your account http://127.0.0.1:8000/verify/{token}'
    send_mail(
        subject=mail_subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to_email],
        fail_silently=False,
    )


@shared_task(bind=True)
def send_mail_forget(self,email1,token):
    to_email = email1
    mail_subject = f'Forget Password Link'
    message = f'Hi, click on the link to change the password of your account http://127.0.0.1:8000/change-password/{token}'
    send_mail(
        subject=mail_subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to_email],
        fail_silently=False,
    )