from django import forms
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from .models import Post, Response
from allauth.account.forms import SignupForm
from string import hexdigits
from django.conf import settings


import random


class PostForm(forms.ModelForm):
    text = forms.CharField(min_length=20)

    class Meta:
        model = Post
        fields = [
            'heading',
            'text',
            'category',
            'image',
            'video',
        ]
        labels = {
            'heading': 'Создайте заголовок',
            'text': 'Введите текст',
            'category': 'Выберите категорию',
            'image': 'Загрузите изображение',
            'video': 'Загрузите видео',
        }

    def clean_name(self):
        heading = self.cleaned_data["heading"]
        if heading[0].islower():
            raise ValidationError(
                "Название должно начинаться с заглавной буквы."
            )
        return heading


class ResponseForm(forms.ModelForm):
    text = forms.CharField(min_length=5)

    class Meta:
        model = Response
        fields = [
            'text',
        ]
        labels = {
            'text': 'Введите текст',
        }


class CommonSignupForm(SignupForm):
    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        user.is_active = False
        code = ''.join(random.sample(hexdigits, 5))
        user.code = code
        user.save()
        send_mail(
            subject=f'Код активации',
            message=f'Код активации аккаунта: {code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email]
        )
        return user
