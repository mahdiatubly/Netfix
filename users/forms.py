from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    password_confirmation = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Customer
        fields = ['email', 'password', 'password_confirmation', 'username', 'date_of_birth']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'password': forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        }
