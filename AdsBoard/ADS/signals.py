from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, Response, Ad, Distribution


@receiver(post_save, sender=Response)
def post_created(instance, created, **kwargs):
    if created:
        ad = instance.ad
        user = ad.author
        email = user.email
        subject = f'Новый отклик'
        text_content = (
            f'Кто-то откликнулся на ваше объявление {instance.ad.head}\n'
            f'Ознакомиться http://127.0.0.1:8000{instance.get_absolute_url()}'
        )
        html_content = (
            f'Кто-то откликнулся на ваше объявление {instance.ad.head}\n<br><br>'
            f'<a href="http://127.0.0.1:8000/ads/responses/">'
            f'Ознакомиться</a>'
        )

        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        print("письмо об отклике отправлено")


@receiver(post_save, sender=Response)
def apply_response(instance, created, **kwargs):
    if not created and not instance.is_active:
        user = instance.user
        email = user.email

        subject = f'Ваш отклик принят'

        text_content = (
            f'Ваш отклик заинтересовал автора объявления: {instance.ad.head}'
        )
        html_content = (
            f'Ваш отклик заинтересовал автора объявления: {instance.ad.head}'
        )

        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        print("письмо о принятии отклика отправлено")


@receiver(post_save, sender=Distribution)
def send_distribution(instance, created, **kwargs):
    if created:
        emails = User.objects.all().values_list('email', flat=True)
        subject = instance.head
        text_content = instance.text
        html_content = instance.text

        msg = EmailMultiAlternatives(subject, text_content, None, [emails])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        print("Рассылка выслана")
