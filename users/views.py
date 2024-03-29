from django.views import generic, View
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.contrib import messages
from services.models import Service, Request
from .models import Customer, Company, UserBase
from .forms import SignupForm, CompanySignupForm, UserProfileUpdateForm, CompanyProfileUpdateForm, RatingForm
from datetime import datetime, timedelta
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse
from django.views.generic.edit import UpdateView
from django.shortcuts import redirect, render
from django.db.models import OuterRef, Subquery
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView as BasePasswordChangeView
from django.contrib.auth.views import PasswordChangeDoneView
from itertools import groupby




class Home(generic.ListView):
    template_name = "users/home.html"
    context_object_name = "most_requested_services"

    def get_queryset(self):
        subquery = (
            Service.objects
            .filter(field=OuterRef('field'))
            .order_by('-requests_count')
            .values('id')[:3]
        )
        queryset = Service.objects.filter(id__in=Subquery(subquery)).order_by('field', '-requests_count')
        grouped_services = {field: list(group) for field, group in groupby(queryset, key=lambda x: x.field)}

        return grouped_services
    
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
    

@method_decorator(login_required, name='dispatch')
class CompetitorsView(View):
    template_name = 'users/competitors.html'

    def get_context_data(self):
        signed_in_company = Company.objects.get(user=self.request.user)
        competitors = Company.objects.filter(field=signed_in_company.field) | Company.objects.filter(field='All in One')
        competitors = competitors.exclude(user=self.request.user)
        competitor_services = Service.objects.filter(company__in=competitors)
        context = {
            'signed_in_company': signed_in_company,
            'competitors': competitors,
            'competitor_services': competitor_services,

        }
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)
    

class CompanyProfileView(LoginRequiredMixin, View):
    template_name = 'users/company_profile.html'

    def get_context_data(self, **kwargs):
        company = get_object_or_404(Company, user=self.request.user)
        services = Service.objects.filter(company=company)
        is_company_owner = True 
        context = {
            'company': company,
            'services': services,
            'is_company_owner': is_company_owner,
        }
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)
    


class PublicCompanyProfileView(View):
    template_name = 'users/company_profile.html'

    def get_context_data(self, **kwargs):
        company = get_object_or_404(Company, user__username=self.kwargs['username'])
        services = Service.objects.filter(company=company)
        context = {
            'company': company,
            'services': services,
        }
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        is_company_owner = context['company'].user == request.user if request.user.is_authenticated else False
        if is_company_owner:
            return redirect(reverse('users:company_profile'))
        return render(request, self.template_name, context)
    
class CompanyListView(ListView):
    model = Company
    template_name = 'users/company_list.html'
    context_object_name = 'companies'


class CustomerProfileView(View):
    template_name = 'users/customer_profile.html'

    def get_context_data(self, **kwargs):
        customer = self.request.user.customer
        active_requests = Request.objects.filter(customer=customer, completed=False)
        previous_requests = Request.objects.filter(customer=customer, completed=True)

        for request in active_requests:
            request.price = request.service.price_hour * request.duration

        for request in previous_requests:
            request.price = request.service.price_hour * request.duration

        context = {
            'customer': customer,
            'active_requests': active_requests,
            'previous_requests': previous_requests,
        }
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)
    
class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserBase
    form_class = UserProfileUpdateForm
    template_name = 'users/update_customer.html'
    success_url = reverse_lazy('users:customer_profile')

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        customer = self.object.customer
        form.initial['date_of_birth'] = customer.date_of_birth
        form.initial['logo'] = customer.logo  
        form.customer_instance = customer
        return form

    def form_valid(self, form):
        date_of_birth = form.cleaned_data['date_of_birth']

        customer = form.customer_instance
        customer.date_of_birth = date_of_birth
        customer.save()

        if 'logo' in self.request.FILES:
            customer.logo = self.request.FILES['logo']
            customer.save()

        return super().form_valid(form)
    
class CompanyProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserBase
    form_class = CompanyProfileUpdateForm
    template_name = 'users/update_company.html'
    success_url = reverse_lazy('users:company_profile')

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        company = self.object.company
        form.initial['field'] = company.field
        form.initial['logo'] = company.logo  
        form.company_instance = company
        return form

    def form_valid(self, form):
        field = form.cleaned_data['field']

        company = form.company_instance
        company.field = field
        company.save()

        if 'logo' in self.request.FILES:
            company.logo = self.request.FILES['logo']
            company.save()

        return super().form_valid(form)
    
class RateServiceView(View):
    template_name = 'users/rate_service.html'

    def get(self, request, *args, **kwargs):
        request_id = self.kwargs.get('pk')
        request_instance = Request.objects.get(pk=request_id)
        form = RatingForm(instance=request_instance)
        return render(request, self.template_name, {'form': form, 'request_instance': request_instance})

    def post(self, request, *args, **kwargs):
        request_id = self.kwargs.get('pk')
        request_instance = Request.objects.get(pk=request_id)
        form = RatingForm(request.POST, instance=request_instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Rating submitted successfully!')
            return redirect('users:customer_profile')
        return render(request, self.template_name, {'form': form, 'request_instance': request_instance})
    
class SearchView(ListView):
    model = Service
    context_object_name = 'search_results'

    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            return Service.objects.filter(name__icontains=query) | \
                   Service.objects.filter(field__icontains=query) | \
                   Service.objects.filter(description__icontains=query)
        return Service.objects.none()

    def get_template_names(self):
        # Get the original template name from the request
        original_template = self.request.GET.get('template', 'users/home.html')
        
        # You may want to validate or sanitize the template name here
        # to prevent potential security issues.

        return [original_template]
    
class CompanySearchView(View):
    template_name = 'users/company_list.html'

    def get(self, request, *args, **kwargs):
        query = request.GET.get('query')
        if query:
            companies = Company.objects.filter(user__username__icontains=query) | \
                        Company.objects.filter(field__icontains=query) 
        else:
            companies = Company.objects.all()

        return render(request, self.template_name, {'companies': companies, 'query': query})

    



    

    


