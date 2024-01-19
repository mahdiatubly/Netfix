from django.urls import path

from . import views

app_name = "services"
urlpatterns = [
    path("company/control/panel", views.ControlPanelView.as_view(), name="control_panel"),
    path("company/create/service", views.ServiceCreateView.as_view(), name="create_service"),
    path('company/services/', views.ServiceListView.as_view(), name='service_list'),
    path('company/services/<int:id>/delete/', views.ServiceDeleteView.as_view(), name='delete_service'),
]