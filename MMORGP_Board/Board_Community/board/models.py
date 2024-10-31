from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from board.services import get_path_upload_image, get_path_upload_video


class User(AbstractUser):
    code = models.CharField(max_length=15, blank=True, null=True)


class Post(models.Model):
    tanks = 'TT'
    healers = 'HL'
    damage_dealers = 'DD'
    dealers = 'DL'
    guild_masters = 'GM'
    quest_givers = 'QG'
    blacksmiths = 'BM'
    tanners = 'TN'
    potion_makers = 'PM'
    spell_masters = 'SM'
    CATEGORIES = [
        ('tanks', 'Танки'),
        ('healers', 'Хилы'),
        ('damage_dealers', 'ДД'),
        ('dealers', 'Торговцы'),
        ('guild_masters', 'Гилдмастеры'),
        ('quest_givers', 'Квестгиверы'),
        ('blacksmiths', 'Кузнецы'),
        ('tanners', 'Кожевники'),
        ('potion_makers', 'Зельевары'),
        ('spell_masters', 'Мастера заклинаний')
    ]
    category = models.CharField(max_length=15, choices=CATEGORIES, verbose_name='Категория')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    datetime_in = models.DateTimeField(auto_now_add=True)
    heading = models.CharField(max_length=60, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    image = models.ImageField(upload_to=get_path_upload_image, null=True, blank=True, verbose_name='Изображение')
    video = models.FileField(upload_to=get_path_upload_video, null=True, blank=True, verbose_name='Видео')

    def preview(self):
        point = '....'
        return self.text[:124] + point

    def __str__(self):
        return f'{self.heading.title()}: {self.text[:10]}'

    def get_absolute_url(self):
        return reverse('ad_detail', args=[str(self.id)])


class Response(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='response')
    text = models.TextField()
    time_response = models.DateTimeField(auto_now_add=True)
    condition = models.BooleanField(default=False)
