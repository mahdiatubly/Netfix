from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse
from .models import Customer
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib import messages
from services.models import Service
from .forms import CustomerForm

class Home(generic.ListView):
    template_name = "users/home.html"
    context_object_name = "most_requested_services"

    def get_queryset(self):
        """Return the last five published questions."""
        return Service.objects.order_by("requests_count")[:5]

class SignupView(CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'users/customer_signup.html'
    success_url = reverse_lazy('users:home')  # Redirect to the home page after successful signup

    def form_valid(self, form):
        # Check if the email is already used
        email = form.cleaned_data['email']
        if Customer.objects.filter(email=email).exists():
            messages.error(self.request, 'Email is already in use.')
            return self.form_invalid(form)

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error in form submission. Please check the form.')
        return super().form_invalid(form)
    

    


