from django import forms
from .models import Account
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class AccountForm(forms.ModelForm):
    """
    Форма для создания (редактирования) учетной записи
    """
    class Meta:
        # с какой моделью связываем форму
        model = Account
        # какие поля нужно отобразить
        fields = ('task', 'note', 'importance', 'deadline')

# Форма РЕГИСТРАЦИИ пользователя
class RegisterForm(UserCreationForm):
    model = User
    fields = ('username',)