from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import datetime


class SignUp(UserCreationForm):
    birth_date = forms.DateField(widget=forms.DateInput())
    picture = forms.ImageField(required=False, widget=forms.FileInput())
    first_name = forms.CharField(required=True,max_length=20)
    last_name = forms.CharField(required=True,max_length=20)
    email = forms.EmailField(required=True,max_length=255)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'picture', 'birth_date')


