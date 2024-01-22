from django.shortcuts import render, redirect
from django.views import View
from .models import Service
from django.urls import reverse_lazy
from users.models import Company, Customer
from .models import Service, Request
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ServiceCreateForm
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ValidationError

class ControlPanelView(LoginRequiredMixin, View):
    template_name = 'services/control_panel.html'

    def get_context_data(self):
        uncompleted_requests = Request.objects.filter(service__company__user=self.request.user, completed=False)
        historical_requests = Request.objects.filter(service__company__user=self.request.user, completed=True)
        comapny_services = Service.objects.filter(company=Company.objects.get(user=self.request.user))[:3]

        context = {
            'uncompleted_requests': uncompleted_requests,
            'historical_requests': historical_requests,
            'comapny_services': comapny_services,
        }
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

class ServiceCreateView(LoginRequiredMixin, CreateView):
    model = Service
    form_class = ServiceCreateForm
    template_name = 'services/create_service.html'
    success_url = reverse_lazy('users:home')

    def form_valid(self, form):
        existing_service = Service.objects.filter(
            name=form.cleaned_data['name'],
            company__user=self.request.user
        ).first()

        if existing_service:
            error_message = "A service with this name already exists."
            return render(self.request, self.template_name, {'form': form, 'error_message': error_message})

        user_company = Company.objects.get(user=self.request.user)

        if user_company.field == 'All in One':
            form.instance.field = form.cleaned_data['field']
        else:
            form.instance.field = user_company.field

        form.instance.company = user_company
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
class ServiceListView(LoginRequiredMixin, ListView):
    model = Service
    template_name = 'services/service_list.html'
    context_object_name = 'services'

    def get_queryset(self):
        return Service.objects.filter(company=Company.objects.get(user=self.request.user))
    
class ServiceDeleteView(LoginRequiredMixin, DeleteView):
    model = Service
    template_name = 'services/service_list.html'  
    success_url = reverse_lazy('services:service_list')  

    def get_object(self, queryset=None):
        service_id = self.kwargs['id']
        return Service.objects.get(id=service_id)
    

class ServiceUpdateView(LoginRequiredMixin, UpdateView):
    model = Service
    form_class = ServiceCreateForm  
    template_name = 'services/update_services.html'
    success_url = reverse_lazy('services:service_list')

    def get_queryset(self):
        return Service.objects.filter(company=Company.objects.get(user=self.request.user))

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user_company = Company.objects.get(user=self.request.user)

        if user_company.field == 'All in One':
            form.fields['field'].widget.attrs['class'] = 'form-control'
        else:
            form.fields.pop('field')

        return form
    
class ClientServiceListView(ListView):
    model = Service
    template_name = 'services/all_services.html'
    context_object_name = 'services'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_company:
            return redirect('users:home')
        return super().get(request, *args, **kwargs)


class ServiceDetailView(View):
    template_name = 'services/service_detail.html'

    def get(self, request, *args, **kwargs):
        service_id = kwargs.get('service_id')
        service = get_object_or_404(Service, id=service_id)
        context = {
            'service': service,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        service_id = kwargs.get('service_id')
        service = get_object_or_404(Service, id=service_id)
        if not request.user.is_authenticated:
            messages.warning(request, 'Please sign in to request this service.')
            return redirect('users:signin')
        if request.user.is_company:
            messages.warning(request, 'Company accounts cannot request services.')
            return redirect('services:service_detail', service_id=service_id)
        customer = get_object_or_404(Customer, user=request.user)
        try:
            Request.objects.create(
                customer=customer,
                service=service,
                date=timezone.now()  
            )
            messages.success(request, 'Request submitted successfully. You will be contacted soon.')
        except Exception as e:
            messages.warning(request, f'Failed to submit request. Error: {str(e)}')
        return redirect('services:service_detail', service_id=service_id)


class CompanyRequestsView(View):
    template_name = 'services/company_requests.html'

    def get_context_data(self, **kwargs):
        company_services = Service.objects.filter(company__user=self.request.user)
        requests = Request.objects.filter(service__in=company_services).order_by('-date')

        context = {
            'requests': requests,
        }
        return context

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_company:
            # Redirect or handle unauthorized access as needed
            return render(request, 'users/unauthorized_access.html')

        context = self.get_context_data()
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_company:
            return render(request, 'users/unauthorized_access.html')

        request_id = kwargs.get('pk')
        if request_id:
            request_instance = Request.objects.filter(pk=request_id, service__company__user=request.user).first()
            if request_instance and not request_instance.completed:
                request_instance.completed = True
                request_instance.save()

        return redirect('services:company_requests') 
    

class MarkRequestCompletedView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, 'users/unauthorized_access.html')

        request_id = kwargs.get('pk')
        if request_id:
            request_instance = Request.objects.filter(pk=request_id, service__company__user=request.user).first()
            if request_instance and not request_instance.completed:
                request_instance.completed = True
                request_instance.save()
            
            request_instance = Request.objects.filter(pk=request_id, customer__user=request.user).first()
            if request_instance and not request_instance.completed:
                request_instance.completed = True
                request_instance.save()
        if not request.user.is_company:
             return redirect('users:customer_profile')
        return redirect('services:company_requests')

