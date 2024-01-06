from django.shortcuts import render
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from django.contrib import messages
from services.models import Service



# users/views.py

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Customer, UserBase
from .forms import SignupForm
from datetime import datetime, timedelta

class Home(generic.ListView):
    template_name = "users/home.html"
    context_object_name = "most_requested_services"

    def get_queryset(self):
        """Return the last five published questions."""
        return Service.objects.order_by("requests_count")[:5]
    


class SignupView(CreateView):
    model = UserBase
    form_class = SignupForm
    template_name = 'users/customer_signup.html'
    success_url = reverse_lazy('users:home')  # Change 'home' to your desired success URL

    def form_valid(self, form):
        # Custom validation logic
        password = form.cleaned_data['password1']
        password_confirmation = form.cleaned_data['password2']

        # Check if password and password confirmation match
        if password != password_confirmation:
            messages.error(self.request, 'Passwords do not match.')
            return self.form_invalid(form)

        # Continue with creating the UserBase and Customer
        user = form.save(commit=False)
        user.set_password(password)
        user.save()

        date_of_birth = form.cleaned_data['date_of_birth']

        customer = Customer.objects.create(user=user, date_of_birth=date_of_birth)
        customer.save()

        return super().form_valid(form)

    def form_invalid(self, form):
        # Custom handling for form validation errors
        return super().form_invalid(form)

# class SignupView(CreateView):
#     model = UserBase
#     form_class = SignupForm
#     template_name = 'users/customer_signup.html'
#     success_url = reverse_lazy('users:home')  # Change 'home' to your desired success URL

#     def form_valid(self, form):
#         password = form.cleaned_data['password']
#         password_confirmation = form.cleaned_data['password_confirmation']

#         # Check if password and password confirmation match
#         if password != password_confirmation:
#             messages.error(self.request, 'Passwords do not match.')
#             return self.form_invalid(form)

#         # Custom validation logic
#         email = form.cleaned_data['email']
#         date_of_birth = form.cleaned_data['date_of_birth']

#         # Check for duplicate email
#         if Customer.objects.filter(user__email=email.lower()).exists():
#             messages.error(self.request, 'Email is already in use.')
#             return self.form_invalid(form)

#         # Check for empty fields
#         if not email or not date_of_birth:
#             messages.error(self.request, 'Please fill in all the required fields.')
#             return self.form_invalid(form)

#         # Check if the age is less than 18
#         today = datetime.now().date()
#         age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
#         if age < 18:
#             messages.error(self.request, 'You must be at least 18 years old to sign up.')
#             return self.form_invalid(form)
        
#         # Continue with creating the UserBase and Customer
#         user = form.save(commit=False)
#         user.set_password(password)
#         user.save()

#         date_of_birth = form.cleaned_data['date_of_birth']

#         customer = Customer.objects.create(user=user)
#         customer.save()

#         return super().form_valid(form)

#     def form_invalid(self, form):
#         # Custom handling for form validation errors
#         return super().form_invalid(form)
    
class SigninView(LoginView):
    template_name = 'users/signin.html'
    # form_class = CustomerForm
    success_url = reverse_lazy('home')

    def form_invalid(self, form):
        messages.error(self.request, 'Incorrect username or password. Please try again.')
        return super().form_invalid(form)
    

    


