from django.urls import path
from django.contrib.auth.views import LogoutView 

from . import views


app_name = "users"
urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("customer/signup", views.SignupView.as_view(), name="customer_signup"),
    path("company/signup", views.CompanySignupView.as_view(), name="company_signup"),
    path('signin/', views.SigninView.as_view(), name='signin'),
    path('signout/', LogoutView.as_view(next_page='users:home'), name='signout'),
    path('competitors/', views.CompetitorsView.as_view(), name='competitors'),
    path('company/profile/', views.CompanyProfileView.as_view(), name='company_profile'),
    path('company/profile/<str:username>/', views.PublicCompanyProfileView.as_view(), name='public_company_profile'),
    path('company/list/', views.CompanyListView.as_view(), name='company_list'),
]