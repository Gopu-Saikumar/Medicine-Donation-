# mediflow/forms.py
from django import forms
from .models import Medicine

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ["name", "category", "quantity", "expiry_date", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Paracetamol 500mg"}),
            "quantity": forms.NumberInput(attrs={"placeholder": "10"}),
            "expiry_date": forms.DateInput(attrs={"type": "date"}),
            "category": forms.Select()
        }
