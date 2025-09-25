from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Address

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'first_name', 'last_name')

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['title', 'first_name', 'last_name', 'phone', 'province',
                 'city', 'address_line', 'postal_code', 'is_default_shipping',
                 'is_default_billing']
        widgets = {
            'address_line': forms.Textarea(attrs={'rows': 3}),
        }