from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=15, help_text='This field is required, maximum length of 15 characters.')
    last_name = forms.CharField(max_length=25, help_text='This field is required, maximum length of 15 characters.')
    email = forms.CharField(max_length=250, help_text='This field is required. Please provide a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)
