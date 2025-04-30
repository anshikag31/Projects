"""
from django.urls import path
from .views import predict_view, patient_dashboard, admin_dashboard
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('predict/', predict_view, name='predict'),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("admin_dashboard/", admin_dashboard, name="admin_dashboard"),
    path("patient_dashboard/", patient_dashboard, name="patient_dashboard"),
]
"""
"""
from django.urls import path, include
from .views import predict_view, patient_dashboard, admin_dashboard
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('predict/', predict_view, name='predict'),
    
    # Authentication URLs
    #path('login/', auth_views.LoginView.as_view(template_name="login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', views.login_view, name='login')

    # Dashboards
    path("admin-dashboard/", admin_dashboard, name="admin_dashboard"),
    path("patient-dashboard/", views.patient_dashboard, name="patient_dashboard"),

    # Include Django authentication URLs (for login, logout, password reset, etc.)
    path('accounts/', include('django.contrib.auth.urls')),
]
"""
from django.contrib.auth import views as auth_views
from django.urls import path
from predictor.views import login_view
from core import views  

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login_view'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('patient_dashboard/', views.patient_dashboard, name='patient_dashboard'),
]



