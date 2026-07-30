from django import forms
from .models import Application


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ("full_name", "email", "university", "course_year", "area", "motivation", "cv")
        labels = {
            "full_name": "Nome Completo",
            "email": "E-mail",
            "university": "Universidade",
            "course_year": "Ano do Curso",
            "area": "Área de Interesse",
            "motivation": "Motivação",
            "cv": "Currículo (CV)",
        }
        widgets = {
            "motivation": forms.Textarea(attrs={"rows": 5,
                "placeholder": "Conta-nos porque queres juntar-te ao Imecx..."}),
        }
