from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from localflavor.us.forms import USStateSelect
from .models import Order, Profile

class CheckoutForm(forms.ModelForm):
    class Meta:
         model = Order
         fields = ['checkout_date', 'due_date']

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    class Meta:
         model = User
         fields = ['first_name', 'last_name', 'username','email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    class Meta:
         model = User
         fields = ['first_name', 'last_name', 'username','email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields =['address1', 'address2', 'city', 'state', 'phone']