from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.core.mail import mail_managers, send_mail
from .models import Response
from django.conf import settings
from django.template.loader import render_to_string


@receiver(post_save, sender=Response)
def notify_about_response(sender, instance, created, **kwargs):
    send_mail(
        subject=f'MMORPG Board',
        message=f'Доброго дня, {instance.post.author}, ! На ваш пост есть новый отклик!\n'
                f'Прочитать отклик:\nhttp://127.0.0.1:8000/board/responses/',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[instance.post.author.email, ],
    )


def notify_about_accept_response(response_id):
    respond = Response.objects.get(id=response_id)
    send_mail(
        subject=f'MMORPG Board',
        message=f'Доброго дня, {respond.user}, ! Ваш отклик приняли!\n'
                f'Прочитать отклик:\nhttp://127.0.0.1:8000/board/responses/',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[respond.user.email, ],
    )
