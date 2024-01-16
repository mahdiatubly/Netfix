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

class ControlPanelView(View):
    template_name = 'services/control_panel.html'

    def get_context_data(self):
        uncompleted_requests = Request.objects.filter(completed=False)[:3]
        historical_requests = Request.objects.filter(completed=True)[:3]

        context = {
            'uncompleted_requests': uncompleted_requests,
            'historical_requests': historical_requests,
        }
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

class ServiceCreateView(LoginRequiredMixin, CreateView):
    model = Service
    form_class = ServiceCreateForm
    template_name = 'services/control_panel.html'  # Replace with your actual template name
    success_url = reverse_lazy('users:home')  # Replace with the URL you want to redirect to upon successful form submission

    def form_valid(self, form):
        # Set the company based on the signed-in user
        form.instance.company = Company.objects.get(user=self.request.user)

        # Automatically set the company field in the Service model
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
    template_name = 'services/service_list.html'  # Create a confirmation template
    success_url = reverse_lazy('services:service_list')  # Redirect to company services page after successful deletion

    def get_object(self, queryset=None):
        # Get the service object based on the provided name (pk) in the URL
        service_name = self.kwargs['name']
        return Service.objects.get(name=service_name)
    

