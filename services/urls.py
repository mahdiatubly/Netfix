from django.urls import path

from . import views

app_name = "services"
urlpatterns = [
    path("control/panel", views.ServiceCreateView.as_view(), name="control_panel"),
]