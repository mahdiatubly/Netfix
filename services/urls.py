from django.urls import path

from . import views

app_name = "services"
urlpatterns = [
    path("company/control/panel", views.ControlPanelView.as_view(), name="control_panel"),
    path("company/create/service", views.ServiceCreateView.as_view(), name="create_service"),
    path('company/services/', views.ServiceListView.as_view(), name='service_list'),
    path('company/services/<int:id>/delete/', views.ServiceDeleteView.as_view(), name='delete_service'),
    path('company/services/<int:pk>/update/', views.ServiceUpdateView.as_view(), name='update_service'),
    path('service/list/', views.ClientServiceListView.as_view(), name='all_services'),
    path('service/<int:service_id>/', views.ServiceDetailView.as_view(), name='service_detail'),
    path('company/requests/', views.CompanyRequestsView.as_view(), name='company_requests'),
    path('mark/request/completed/<int:pk>/', views.MarkRequestCompletedView.as_view(), name='mark_request_completed'),
    path('services/<str:field>/', views.FieldServicesView.as_view(), name='field_services'),





]