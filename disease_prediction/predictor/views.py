from django.shortcuts import render
from django.http import JsonResponse
import json
import pandas as pd
import numpy as np
import joblib
import os
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.decorators import login_required
from pathlib import Path

# Define BASE_DIR dynamically
BASE_DIR = Path(__file__).resolve().parent.parent
PREDICTOR_DIR = BASE_DIR / "predictor"

# Load trained model & preprocessing objects
try:
    model_path = PREDICTOR_DIR / "best_model.pkl"
    scaler_path = PREDICTOR_DIR / "scaler.pkl"
    encoder_path = PREDICTOR_DIR / "label_encoder.pkl"
    features_path = PREDICTOR_DIR / "feature_columns.pkl"

    if not all(path.exists() for path in [model_path, scaler_path, encoder_path, features_path]):
        raise FileNotFoundError("One or more model files are missing!")

    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    label_encoder = joblib.load(encoder_path)
    feature_columns = joblib.load(features_path)

except Exception as e:
    print(f"❌ Error loading model or preprocessing objects: {e}")
    feature_columns = [] 

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse

def login_view(request):
    if request.method == "POST":
        role = request.POST.get("role")  # Get user role from the dropdown
        if role == "patient":
            return redirect("predict")  # Redirect patients directly to predict page

        # Process admin login
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:  # Ensure only admin users log in
            login(request, user)
            return redirect(reverse("admin:index"))  # Redirect explicitly to Django Admin Panel
        
        return render(request, "predictor/login.html", {"error": "Invalid admin credentials"})

    return render(request, "predictor/login.html")

    

@login_required
def patient_dashboard(request):
    return render(request, "predictor/predict.html")

@login_required
def admin_dashboard(request):
    #predictions = Prediction.objects.all()
    return render(request, "predictor/admin_dashboard.html")
                  #, {"predictions": predictions})

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('login')  # Ensure 'login' is the correct name in urls.py


def predict_disease(request):
    
    if request.method == "POST":
        try:
            if not feature_columns:
                return JsonResponse({"error": "Feature columns not loaded. Check feature_columns.pkl."})

            data = request.POST
            selected_symptoms = [data.get(f"Symptom_{i}") for i in range(1, 6) if data.get(f"Symptom_{i}")]

            symptoms_list = [0] * len(feature_columns)
            for symptom in selected_symptoms:
                if symptom in feature_columns:
                    symptoms_list[feature_columns.index(symptom)] = 1

            if not any(symptoms_list):
                return JsonResponse({"error": "No symptoms selected!"})

            input_df = pd.DataFrame([symptoms_list], columns=feature_columns)
            input_scaled = scaler.transform(input_df)
            prediction = model.predict(input_scaled)[0]
            disease_name = label_encoder.inverse_transform([prediction])[0]

            return JsonResponse({"disease": disease_name})

        except Exception as e:
            return JsonResponse({"error": str(e)})

    return render(request, 'predictor/predict.html')