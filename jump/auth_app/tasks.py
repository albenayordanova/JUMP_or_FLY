from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

UserModel = get_user_model()


@shared_task
def send_successful_registration_email(user_pk):
    user = UserModel.objects.get(pk=user_pk)
    send_mail(
        'Hello from us!',
        'Welcome to our site!',
        'foso@abv.bg',
        (user.email,),
    )
