from django import forms
from .models import User


class SignupForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'gender']
        labels = {
            'username': 'Enter Username',
            'email': 'Enter Email',
            'password': 'Enter Password',
            'gender': 'Select Gender'
            }
        error_messages = {
            'username': {
             'required': 'This field is required',
             'max_length': 'Max length should not exceed'
            }
        }
        widgets = {
            'password': forms.PasswordInput()
        }


class LoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'password']
        labels = {
            'username': 'Enter Username',
            'password': 'Enter Password'
        }
        widgets = {
            'password': forms.PasswordInput()
        }
