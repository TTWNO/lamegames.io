from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import LameUser

class LameUserSignupForm(UserCreationForm):
    email = forms.EmailField(max_length=100, help_text='Required')
    class Meta:
        model = LameUser
        fields = ('username', 'email', 'password1', 'password2')