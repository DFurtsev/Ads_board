from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.urls import reverse



class User(AbstractUser):
    code = models.CharField(max_length=15, blank=True, null=True)


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name.title()


class Ad(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    publication_time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='AdCategory')
    head = models.CharField(max_length=255)
    text = RichTextUploadingField()
    # file = models.FileField(upload_to='uploads/')

    def get_absolute_url(self):
        return reverse('ads')

    def __str__(self):
        return self.head.title()


class AdCategory(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Response(models.Model):
    text = models.CharField(max_length=255, null=True)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, verbose_name='Объявление')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('ads')


class Distribution(models.Model):
    head = models.CharField(max_length=255)
    text = RichTextUploadingField()


