from django.urls import path
from django.contrib.auth.views import LogoutView 
from django.contrib.auth import views as auth_views

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
    path('customer/profile/', views.CustomerProfileView.as_view(), name='customer_profile'),
    path('update/customer/', views.UserProfileUpdateView.as_view(), name='update_customer'),
    path('update/company/', views.CompanyProfileUpdateView.as_view(), name='update_company'),
    path('<int:pk>/password/', auth_views.PasswordChangeView.as_view(
        template_name='users/change_password.html',
        success_url='/users/change_password_done/'  
    ), name='change_password'),
    path('change_password_done/', views.PasswordChangeDoneView.as_view(
        template_name='users/change_password_done.html'
    ), name='change_password_done'),
    path('rate_service/<int:pk>/', views.RateServiceView.as_view(), name='rate_service'),


]

