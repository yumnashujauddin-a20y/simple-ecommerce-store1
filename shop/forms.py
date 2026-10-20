from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Order


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]


class CheckoutForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = [
            "full_name",
            "email",
            "phone",
            "address",
        ]

        widgets = {
            "full_name": forms.TextInput(
                attrs={
                    "placeholder": "Enter your full name"
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "placeholder": "Enter your email"
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "placeholder": "Enter your phone number"
                }
            ),

            "address": forms.Textarea(
                attrs={
                    "placeholder": "Enter your complete address",
                    "rows": 4
                }
            ),
        }