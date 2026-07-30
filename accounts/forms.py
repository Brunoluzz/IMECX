from django import forms
from django.contrib.auth import get_user_model

from .models import Profile

User = get_user_model()


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="Email")
    
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["phone", "bio"]
        widgets = {
            "phone": forms.TextInput(attrs={"placeholder": "+351 ..."}),
            "bio": forms.Textarea(attrs={"rows": 4}),
        }