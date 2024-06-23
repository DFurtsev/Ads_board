import random
from string import hexdigits
from django.conf import settings
from django.core.mail import send_mail

from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = "Введите адрес вашей почты"

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.is_active = False
        code = ''.join(random.sample(hexdigits, 5))
        user.code = code
        print(user.code)
        users = Group.objects.get(name="Users")
        user.groups.add(users)
        user.save()
        print(user.code)
        send_mail(
            subject='Код активации',
            message=f'Код подтверждения для вашего аккаунта: {code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        return user