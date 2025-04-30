from django import forms
from .models import Patient, Prediction

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'gender', 'dob','email']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }

class PredictionForm(forms.ModelForm):
    symptom1 = forms.CharField(max_length=100, required=True, label="Symptom 1")
    symptom2 = forms.CharField(max_length=100, required=True, label="Symptom 2")
    symptom3 = forms.CharField(max_length=100, required=True, label="Symptom 3")

    class Meta:
        model = Prediction
        fields = ['symptoms']
        widgets = {
            'symptoms': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        symptoms = [cleaned_data.get("symptom1"), cleaned_data.get("symptom2"), cleaned_data.get("symptom3")]
        cleaned_data["symptoms"] = ', '.join(filter(None, symptoms))  # Store symptoms as a single text field
        return cleaned_data
