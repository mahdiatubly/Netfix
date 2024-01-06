# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MinValueValidator
from datetime import date
from .models import UserBase

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), validators=[MinValueValidator(limit_value=date(1900, 1, 1))])
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password')

    class Meta:
        model = UserBase
        fields = ['username', 'email', 'date_of_birth', 'password1', 'password2']
