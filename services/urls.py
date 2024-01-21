from django.urls import path

from . import views

app_name = "services"
urlpatterns = [
    path("company/control/panel", views.ControlPanelView.as_view(), name="control_panel"),
    path("company/create/service", views.ServiceCreateView.as_view(), name="create_service"),
    path('company/services/', views.ServiceListView.as_view(), name='service_list'),
    path('company/services/<int:id>/delete/', views.ServiceDeleteView.as_view(), name='delete_service'),
    path('company/services/<int:pk>/update/', views.ServiceUpdateView.as_view(), name='update_service'),
    path('service-list/', views.ClientServiceListView.as_view(), name='all_services'),
    path('service/<int:service_id>/', views.ServiceDetailView.as_view(), name='service_detail'),


]