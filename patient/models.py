from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

from .validators import PhoneRegexValidator


class Patient(models.Model):
    MALE_CHOICE = 'male'
    FEMALE_CHOICE = 'female'

    SEX_CHOICES = (
        (MALE_CHOICE, 'Мужчина'),
        (FEMALE_CHOICE, 'Женщина')
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пациент',
        null=True
    )
    firstname = models.CharField(
        max_length=255,
        verbose_name='Имя',
        null=True,
        default=''
    )
    lastname = models.CharField(
        max_length=255,
        verbose_name='Фамилия',
        null=True,
        default=''
    )
    sex = models.CharField(
        verbose_name="Пол",
        max_length=50,
        choices=SEX_CHOICES,
        null=True,
        default=''
    )
    date_of_birth = models.DateField(
        verbose_name="День рождения",
        null=True,
        default=datetime.now
    )
    phone = models.CharField(
        max_length=255,
        verbose_name='Телефон',
        validators=[PhoneRegexValidator()],
        null=True,
        default=''
    )
    email = models.EmailField(
        max_length=255,
        verbose_name='Email для связи'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания',
    )
    tos = models.BooleanField(
        default=False
    )

    def get_age(self):
        return datetime.now().year - self.date_of_birth.year

    class Meta:
        verbose_name = 'Пациент'
        verbose_name_plural = 'Пациент'

    def __str__(self):
        return f"{self.firstname} {self.lastname}"
