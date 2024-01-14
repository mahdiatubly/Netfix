from django.views import generic
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from django.contrib import messages
from services.models import Service
from .models import Customer, Company, UserBase
from .forms import SignupForm, CompanySignupForm
from datetime import datetime, timedelta
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect

class Home(generic.ListView):
    template_name = "users/home.html"
    context_object_name = "most_requested_services"

    def get_queryset(self):
        """Return the last five published questions."""
        return Service.objects.order_by("requests_count")[:5]
class SignupView(UserPassesTestMixin, CreateView):
    model = UserBase
    form_class = SignupForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('users:home')

    def test_func(self):
        return not self.request.user.is_authenticated
    
    def handle_no_permission(self):
        return redirect('users:home') 

    def form_valid(self, form):
        password = form.cleaned_data['password1']
        password_confirmation = form.cleaned_data['password2']

        if password != password_confirmation:
            messages.error(self.request, 'Passwords do not match.')
            return self.form_invalid(form)
        
        date_of_birth = form.cleaned_data['date_of_birth']

        today = datetime.now().date()
        age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
        if age < 18:
            messages.error(self.request, 'You must be at least 18 years old to sign up.')
            return self.form_invalid(form)

        user = form.save(commit=False)
        user.set_password(password)
        user.save()

        customer = Customer.objects.create(user=user, date_of_birth=date_of_birth)
        customer.save()

        return super().form_valid(form)
    
class CompanySignupView(UserPassesTestMixin, CreateView):
    model = UserBase
    form_class = CompanySignupForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('users:home')

    def test_func(self):
        # Check if the user is not authenticated
        return not self.request.user.is_authenticated
    
    def handle_no_permission(self):
        return redirect('users:home')

    def form_valid(self, form):
        password = form.cleaned_data['password1']
        password_confirmation = form.cleaned_data['password2']

        if password != password_confirmation:
            messages.error(self.request, 'Passwords do not match.')
            return self.form_invalid(form)
        
        field = form.cleaned_data['field']
        form.instance.is_company = True

        user = form.save(commit=False)
        user.set_password(password)
        user.save()

        company = Company.objects.create(user=user, field=field)
        company.save()

        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)
    


class SigninView(UserPassesTestMixin, LoginView):
    template_name = 'users/signin.html'
    success_url = reverse_lazy('users:home')

    def test_func(self):
        return not self.request.user.is_authenticated
    
    def handle_no_permission(self):
        return redirect('users:home')
    



    

    


