"""
from django.shortcuts import render

import joblib
import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse

# Load trained model and label encoder
model = joblib.load('predictor/best_model.pkl')  # Ensure correct path
label_encoder = joblib.load('predictor/label_encoder.pkl')

# Define all 132 symptom names (update this based on your dataset's column names)
SYMPTOMS = [
    "itching", "skin_rash", "nodal_skin_eruptions", "continuous_sneezing", "shivering", "chills", "joint_pain", 
    "stomach_pain", "acidity", "ulcers_on_tongue", "muscle_wasting", "vomiting", "burning_micturition", 
    "spotting_urination", "fatigue", "weight_gain", "anxiety", "cold_hands_and_feets", "mood_swings", "weight_loss", 
    "restlessness", "lethargy", "patches_in_throat", "irregular_sugar_level", "cough", "high_fever", "sunken_eyes", 
    "breathlessness", "sweating", "dehydration", "indigestion", "headache", "yellowish_skin", "dark_urine", "nausea", 
    "loss_of_appetite", "pain_behind_the_eyes", "back_pain", "constipation", "abdominal_pain", "diarrhoea", 
    "mild_fever", "yellow_urine", "yellowing_of_eyes", "acute_liver_failure", "fluid_overload", "swelling_of_stomach", 
    "swelled_lymph_nodes", "malaise", "blurred_and_distorted_vision", "phlegm", "throat_irritation", "redness_of_eyes", 
    "sinus_pressure", "runny_nose", "congestion", "chest_pain", "weakness_in_limbs", "fast_heart_rate", 
    "pain_during_bowel_movements", "pain_in_anal_region", "bloody_stool", "irritation_in_anus", "neck_pain", "dizziness", 
    "cramps", "bruising", "obesity", "swollen_legs", "swollen_blood_vessels", "puffy_face_and_eyes", "enlarged_thyroid", 
    "brittle_nails", "swollen_extremeties", "excessive_hunger", "extra_marital_contacts", "drying_and_tingling_lips", 
    "slurred_speech", "knee_pain", "hip_joint_pain", "muscle_weakness", "stiff_neck", "swelling_joints", 
    "movement_stiffness", "spinning_movements", "loss_of_balance", "unsteadiness", "weakness_of_one_body_side", 
    "loss_of_smell", "bladder_discomfort", "foul_smell_of_urine", "continuous_feel_of_urine", "passage_of_gases", 
    "internal_itching", "toxic_look_(typhos)", "depression", "irritability", "muscle_pain", "altered_sensorium", 
    "red_spots_over_body", "belly_pain", "abnormal_menstruation", "dischromic_patches", "watering_from_eyes", 
    "increased_appetite", "polyuria", "family_history", "mucoid_sputum", "rusty_sputum", "lack_of_concentration", 
    "visual_disturbances", "receiving_blood_transfusion", "receiving_unsterile_injections", "coma", "stomach_bleeding", 
    "distention_of_abdomen", "history_of_alcohol_consumption", "fluid_overload", "blood_in_sputum", 
    "prominent_veins_on_calf", "palpitations", "painful_walking", "pus_filled_pimples", "blackheads", "scurring", 
    "skin_peeling", "silver_like_dusting", "small_dents_in_nails", "inflammatory_nails", "blister", 
    "red_sore_around_nose", "yellow_crust_ooze"
]


def predict_disease(request):
    if request.method == "POST":
        try:
            data = request.POST  # Get data from frontend
            input_data = [int(data.get(symptom, 0)) for symptom in SYMPTOMS]  # Convert to list
            
            # Create a DataFrame with the correct column names
            input_df = pd.DataFrame([input_data], columns=SYMPTOMS)
            
            # Predict disease
            prediction = model.predict(input_df)[0]
            disease_name = label_encoder.inverse_transform([prediction])[0]

            return JsonResponse({"disease": disease_name})

        except Exception as e:
            return JsonResponse({"error": str(e)})

    return render(request, 'predictor/predict.html')
    """
"""
import pandas as pd
import numpy as np
import joblib

# Load trained model & preprocessing objects
model = joblib.load('predictor/best_model.pkl')
scaler = joblib.load('predictor/scaler.pkl')
label_encoder = joblib.load('predictor/label_encoder.pkl')
feature_columns = joblib.load('predictor/feature_columns.pkl')  # Load saved feature names

def predict_disease(symptoms_list):
    # Convert input into DataFrame
    input_data = pd.DataFrame([symptoms_list], columns=feature_columns)  # Ensure column order
    input_data = input_data.astype(float)

    # Apply same scaling
    input_scaled = scaler.transform(input_data)

    # Predict disease
    prediction = model.predict(input_scaled)
    disease = label_encoder.inverse_transform(prediction)[0]  # Convert label back to disease name
    return disease

# Example usage
if __name__ == "__main__":
    example_symptoms = [0] * len(feature_columns)  # Replace with real user input
    print("Predicted Disease:", predict_disease(example_symptoms))
"""
"""

from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
import numpy as np
import joblib

# Load trained model & preprocessing objects
model = joblib.load('predictor/best_model.pkl')
scaler = joblib.load('predictor/scaler.pkl')
label_encoder = joblib.load('predictor/label_encoder.pkl')
feature_columns = joblib.load('predictor/feature_columns.pkl')  # Load saved feature names

def predict_disease(request):
    if request.method == "POST":
        try:
            data = request.POST  # Get form data
            print("Received Data:", data)  # Debugging step

            # Extract symptoms as binary list (1 for selected, 0 otherwise)
            symptoms_list = [int(data.get(symptom, 0)) for symptom in feature_columns]
            print("Processed Symptoms:", symptoms_list)  # Debugging step

            if not any(symptoms_list):  # Check if all symptoms are 0
                return JsonResponse({"error": "No symptoms selected!"})

            # Convert to DataFrame with correct columns
            input_df = pd.DataFrame([symptoms_list], columns=feature_columns)
            input_df = input_df.astype(float)  # Ensure correct dtype

            # Apply the same scaling as during training
            input_scaled = scaler.transform(input_df)

            # Predict the disease
            prediction = model.predict(input_scaled)[0]
            disease_name = label_encoder.inverse_transform([prediction])[0]

            return JsonResponse({"disease": disease_name})

        except Exception as e:
            print("Error:", str(e))  # Debugging step
            return JsonResponse({"error": str(e)})

    return render(request, 'predictor/predict.html')
    """
"""
from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
import numpy as np
import joblib
import os  # Added to check file existence

# Load trained model & preprocessing objects
try:
    model_path = 'best_model.pkl'
    scaler_path = 'scaler.pkl'
    encoder_path = 'label_encoder.pkl'
    features_path = 'feature_columns.pkl'

    if not all(os.path.exists(path) for path in [model_path, scaler_path, encoder_path, features_path]):
        raise FileNotFoundError("One or more model files are missing!")

    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    label_encoder = joblib.load(encoder_path)
    feature_columns = joblib.load(features_path)

    print("✅ Model and preprocessing files loaded successfully.")
    print("🔹 Feature Columns:", feature_columns)  # Debugging: Print feature columns
except Exception as e:
    print(f"❌ Error loading model or preprocessing objects: {e}")
    feature_columns = []  # Ensure it is defined even if loading fails

def predict_disease(request):
    if request.method == "POST":
        try:
            if not feature_columns:  # Ensure feature_columns is loaded
                return JsonResponse({"error": "Feature columns not loaded. Check feature_columns.pkl."})

            data = request.POST
            print("📥 Received Data:", data)  # Debugging

            # Extract symptoms from request
            selected_symptoms = [data.get(f"Symptom_{i}") for i in range(1, 6) if data.get(f"Symptom_{i}")]
            print("🔹 Selected Symptoms:", selected_symptoms)  # Debugging

            # Initialize feature vector with zeros
            symptoms_list = [0] * len(feature_columns)

            # Map selected symptoms to feature_columns
            for symptom in selected_symptoms:
                if symptom in feature_columns:
                    index = feature_columns.index(symptom)
                    symptoms_list[index] = 1
                else:
                    print(f"⚠️ Warning: {symptom} not found in feature_columns list")

            print("🔹 Processed Symptoms Vector:", symptoms_list)  # Debugging

            if not any(symptoms_list):
                return JsonResponse({"error": "No symptoms selected!"})

            # Convert to DataFrame
            input_df = pd.DataFrame([symptoms_list], columns=feature_columns)

            # Scale input data
            input_scaled = scaler.transform(input_df)

            # Predict disease
            prediction = model.predict(input_scaled)[0]
            disease_name = label_encoder.inverse_transform([prediction])[0]

            return JsonResponse({"disease": disease_name})

        except Exception as e:
            print(f"❌ Error: {e}")
            return JsonResponse({"error": str(e)})

    return render(request, 'predictor/predict.html')
"""
from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
import numpy as np
import joblib
import os  # Added to check file existence

# Get the absolute path of the predictor app
BASE_DIR = "C:/Users/KIIT/Documents/Major/disease_prediction"
PREDICTOR_DIR = os.path.join(BASE_DIR, "predictor")  # Path to predictor app

# Load trained model & preprocessing objects
try:
    model_path = os.path.join(PREDICTOR_DIR, "best_model.pkl")
    scaler_path = os.path.join(PREDICTOR_DIR, "scaler.pkl")
    encoder_path = os.path.join(PREDICTOR_DIR, "label_encoder.pkl")
    features_path = os.path.join(PREDICTOR_DIR, "feature_columns.pkl")

    print("🔍 Checking file existence:")
    print(f"📂 Model exists: {os.path.exists(model_path)} | Path: {model_path}")
    print(f"📂 Scaler exists: {os.path.exists(scaler_path)} | Path: {scaler_path}")
    print(f"📂 Encoder exists: {os.path.exists(encoder_path)} | Path: {encoder_path}")
    print(f"📂 Feature Columns exist: {os.path.exists(features_path)} | Path: {features_path}")

    if not all(os.path.exists(path) for path in [model_path, scaler_path, encoder_path, features_path]):
        raise FileNotFoundError("One or more model files are missing!")

    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    label_encoder = joblib.load(encoder_path)
    feature_columns = joblib.load(features_path)

    print("✅ Model and preprocessing files loaded successfully.")
    print("🔹 Feature Columns:", feature_columns)  # Debugging: Print feature columns
except Exception as e:
    print(f"❌ Error loading model or preprocessing objects: {e}")
    feature_columns = []  # Ensure it is defined even if loading fails

def predict_disease(request):
    if request.method == "POST":
        try:
            if not feature_columns:  # Ensure feature_columns is loaded
                return JsonResponse({"error": "Feature columns not loaded. Check feature_columns.pkl."})

            data = request.POST
            print("📥 Received Data:", data)  # Debugging

            # Extract symptoms from request
            selected_symptoms = [data.get(f"Symptom_{i}") for i in range(1, 6) if data.get(f"Symptom_{i}")]
            print("🔹 Selected Symptoms:", selected_symptoms)  # Debugging

            # Initialize feature vector with zeros
            symptoms_list = [0] * len(feature_columns)

            # Map selected symptoms to feature_columns
            for symptom in selected_symptoms:
                if symptom in feature_columns:
                    index = feature_columns.index(symptom)
                    symptoms_list[index] = 1
                else:
                    print(f"⚠️ Warning: {symptom} not found in feature_columns list")

            print("🔹 Processed Symptoms Vector:", symptoms_list)  # Debugging

            if not any(symptoms_list):
                return JsonResponse({"error": "No symptoms selected!"})

            # Convert to DataFrame
            input_df = pd.DataFrame([symptoms_list], columns=feature_columns)

            # Scale input data
            input_scaled = scaler.transform(input_df)

            # Predict disease
            prediction = model.predict(input_scaled)[0]
            disease_name = label_encoder.inverse_transform([prediction])[0]

            return JsonResponse({"disease": disease_name})

        except Exception as e:
            print(f"❌ Error: {e}")
            return JsonResponse({"error": str(e)})

    return render(request, 'predictor/predict.html')



