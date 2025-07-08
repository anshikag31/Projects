"""
from django.urls import path
from predictor import views  
from django.contrib.auth import views as auth_views
from predictor.views import login_view

urlpatterns = [
    path("", views.login_view, name="home"),  # Redirect "/" to login page
    path("login/", views.login_view, name="login"),
    path("patient_dashboard/", views.patient_dashboard, name="patient_dashboard"),
    path("admin_dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("predict/", views.predict_disease, name="predict"),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]
"""


from django.urls import path
from .views import login_view, logout_view, patient_dashboard, admin_dashboard, predict_disease

urlpatterns = [
    path("login/", login_view, name="login_view"),
    path("logout/", logout_view, name="logout"),
    path("patient-dashboard/", patient_dashboard, name="patient_dashboard"),
    path("admin-dashboard/", admin_dashboard, name="admin_dashboard"),
    path("predict/", predict_disease, name="predict"),
]