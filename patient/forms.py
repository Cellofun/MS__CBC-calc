from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from datetime import datetime

from .models import Patient


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Имя пользователя',
                'class': 'form-control h-auto text-white placeholder-white opacity-70 bg-dark-o-70 rounded-pill border-0 py-4 px-8 mb-5',
            }
        )
    )
    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Пароль',
                'class': 'form-control h-auto text-white placeholder-white opacity-70 bg-dark-o-70 rounded-pill border-0 py-4 px-8 mb-5',
            }
        )
    )

    class Meta:
        model = User
        fields = ('username', 'password')


class RegistrationForm(UserCreationForm):
    SEX = ''
    MALE_CHOICE = 'male'
    FEMALE_CHOICE = 'female'

    SEX_CHOICES = (
        (SEX, 'Пол'),
        (MALE_CHOICE, 'Мужской'),
        (FEMALE_CHOICE, 'Женский')
    )

    username = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Имя пользователя',
                'class': 'form-control h-auto text-white placeholder-white opacity-70 bg-dark-o-70 rounded-pill border-0 py-4 px-8 mb-5',
            }
        )
    )
    password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Пароль',
                'class': 'form-control h-auto text-white placeholder-white opacity-70 bg-dark-o-70 rounded-pill border-0 py-4 px-8 mb-5',
            }
        )
    )
    password2 = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Подтверждение пароля',
                'class': 'form-control h-auto text-white placeholder-white opacity-70 bg-dark-o-70 rounded-pill border-0 py-4 px-8 mb-5',
            }
        )
    )
    email = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'E-mail',
                'class': 'form-control h-auto text-white placeholder-white opacity-70 bg-dark-o-70 rounded-pill border-0 py-4 px-8 mb-5',
            }
        )
    )
    date_of_birth = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'День рождения',
                'class': 'form-control h-auto text-white placeholder-white opacity-70 bg-dark-o-70 rounded-pill border-0 py-4 px-8 mb-5',
            }
        )
    )
    sex = forms.ChoiceField(
        choices=SEX_CHOICES,
        label='',
        widget=forms.Select(
            attrs={
                'class': 'form-control h-auto text-white placeholder-white opacity-70 bg-dark-o-70 rounded-pill border-0 py-4 px-8 mb-5',
            }
        )
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'date_of_birth', 'sex')

    def save(self, **kwargs):
        user = super().save()

        Patient.objects.create(
            user=user,
            email=self.cleaned_data["email"],
            date_of_birth=datetime.strptime(self.cleaned_data["date_of_birth"], '%d.%m.%Y'),
            sex=self.cleaned_data["sex"]
        )
        return user

    def clean(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        sex = self.cleaned_data.get('email')
        errors = {}

        if User.objects.filter(username=username).exists():
            errors['username'] = ValidationError("Пользователь с таким именем уже существует.")

        if User.objects.filter(email=email).exists():
            errors['email'] = ValidationError("Пользователь с таким email уже существует.")

        if sex == '':
            errors['sex'] = ValidationError("Пожалуйста, укажите пол.")

        if errors:
            raise ValidationError(errors)

        return self.cleaned_data


class EditProfileForm(ModelForm):
    email = forms.CharField(
        label="E-mail"
    )
    phone = forms.CharField(
        label="Контактный телефон",
        required=False
    )
    firstname = forms.CharField(
        label="Имя",
        required=False
    )
    lastname = forms.CharField(
        label="Фамилия",
        required=False,
    )
    sex = forms.ChoiceField(
        label="Пол",
        choices=Patient.SEX_CHOICES
    )
    date_of_birth = forms.DateField(
        label="День рождения",
        widget=forms.DateInput(
            attrs={
                'type': 'text',
                'id': 'date_of_birth',
                'readonly': '',
                'placeholder': ''
            })
        )

    class Meta:
        model = Patient
        fields = ('firstname', 'lastname', 'date_of_birth', 'sex', 'email', 'phone')

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.label_suffix = ""
