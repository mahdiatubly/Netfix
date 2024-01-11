from django.urls import path

from . import views


app_name = "users"
urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("customer/signup", views.SignupView.as_view(), name="customer_signup"),
    path("company/signup", views.CompanySignupView.as_view(), name="company_signup"),
    path('signin/', views.SigninView.as_view(), name='signin'),
]