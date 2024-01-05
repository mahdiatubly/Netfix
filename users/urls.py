from django.urls import path

from . import views


app_name = "users"
urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("customer/signup", views.SignupView.as_view(), name="customer_signup"),
]