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

class CompanySignupForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    field = forms.ChoiceField(choices=(('Air Conditioner', 'Air Conditioner'),
                                                     ('All in One', 'All in One'),
                                                     ('Carpentry', 'Carpentry'),
                                                     ('Electricity',
                                                      'Electricity'),
                                                     ('Gardening', 'Gardening'),
                                                     ('Home Machines',
                                                      'Home Machines'),
                                                     ('House Keeping',
                                                      'House Keeping'),
                                                     ('Interior Design',
                                                      'Interior Design'),
                                                     ('Locks', 'Locks'),
                                                     ('Painting', 'Painting'),
                                                     ('Plumbing', 'Plumbing'),
                                                     ('Water Heaters', 'Water Heaters')), widget=forms.Select(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password')
    username = forms.CharField(label="Company Name")
    

    class Meta:
        model = UserBase
        fields = ['username', 'email', 'field', 'password1', 'password2']