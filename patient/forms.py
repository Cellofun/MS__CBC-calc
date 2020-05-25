from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm

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
                'placeholder': 'Повтор пароля',
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

    class Meta:
        model = User
        fields = ('username', 'email')

    def save(self, **kwargs):
        user = super().save()

        Patient.objects.create(
            user=user,
            email=self.cleaned_data["email"],
        )
        return user

    def clean(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже существует.")
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
        required=False,
        choices=Patient.SEX_CHOICES
    )
    date_of_birth = forms.DateField(
        label="День рождения",
        required=False,
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
