from django.urls import path
from .views import predict_disease  # Ensure you import the correct function from views.py

urlpatterns = [
    path('predict/', predict_disease, name='predict'),
]
