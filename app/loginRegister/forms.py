from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class AddUserForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": 'form-control', 'placeholder': 'Login'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": 'form-control', 'placeholder': 'Password'}))

class CreateUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": 'form-control', 'placeholder': 'Login'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={"class": 'form-control', 'placeholder': 'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": 'form-control', 'placeholder': 'Password Again'}))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')