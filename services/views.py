from django.shortcuts import render, redirect
from django.views import View
from .models import Service
from django.urls import reverse_lazy
from users.models import Company
from .models import Service, Request
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ServiceCreateForm
from django.views.generic.edit import DeleteView
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError

class ControlPanelView(LoginRequiredMixin, View):
    template_name = 'services/control_panel.html'

    def get_context_data(self):
        uncompleted_requests = Request.objects.filter(completed=False)[:3]
        historical_requests = Request.objects.filter(completed=True)[:3]
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

        form.instance.company = Company.objects.get(user=self.request.user)
        form.instance.field = Company.objects.get(user=self.request.user).field
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
    

