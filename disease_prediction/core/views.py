import joblib
import os
from pathlib import Path
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Prediction, Patient

# Define BASE_DIR dynamically
BASE_DIR = Path(__file__).resolve().parent.parent
PREDICTOR_DIR = BASE_DIR / 'predictor'
MODEL_PATH = PREDICTOR_DIR / 'random_forest.pkl'

try:
    rf_model = joblib.load(MODEL_PATH)
except Exception as e:
    print(f"❌ Error loading RandomForest model: {e}")

symptoms_list = [ ... ]  # Keep your existing symptoms list

symptom_index = {symptom: idx for idx, symptom in enumerate(symptoms_list)}

def predict_view(request):
    if request.method == "POST":
        symptom1 = request.POST.get("Symptom_1", "")
        symptom2 = request.POST.get("Symptom_2", "")
        symptom3 = request.POST.get("Symptom_3", "")

        if not all([symptom1, symptom2, symptom3]):
            return JsonResponse({"error": "Please select all three symptoms."})

        symptoms_vector = [0] * len(symptom_index)
        try:
            symptoms_vector[symptom_index[symptom1]] = 1
            symptoms_vector[symptom_index[symptom2]] = 1
            symptoms_vector[symptom_index[symptom3]] = 1
        except KeyError:
            return JsonResponse({"error": "Invalid symptoms selected."})

        try:
            predicted_disease = rf_model.predict([symptoms_vector])[0]
            Prediction.objects.create(
                symptoms=f"{symptom1}, {symptom2}, {symptom3}",
                predicted_disease=predicted_disease
            )
            return JsonResponse({"disease": predicted_disease})
        except Exception as e:
            return JsonResponse({"error": f"Prediction error: {e}"})

    return render(request, "predict.html")

@login_required
def patient_dashboard(request):
    return render(request, 'predictor/patient_dashboard.html')

@login_required
def admin_dashboard(request):
    patients = Patient.objects.all()
    return render(request, 'predictor/admin_dashboard.html', {'patients': patients})