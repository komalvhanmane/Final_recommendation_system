from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class SignUpForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control w-50'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control w-50'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {'first_name': 'First Name', 'last_name': 'Last Name', 'email': 'Email Address'}
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control w-50'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control w-50'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control w-50'}),
            'email': forms.EmailInput(attrs={'class': 'form-control w-50'}),
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control w-50'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control w-50'}))

    class Meta:
        fields = ['username', 'password']

