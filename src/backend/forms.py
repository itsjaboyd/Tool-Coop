from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from localflavor.us.forms import USStateSelect
from .models import Order, Profile, ToolType


USER_CHOICES= [tuple([user.id,user.username]) for user in User.objects.filter(is_superuser=False)]

class CheckoutForm(forms.Form):
    print(USER_CHOICES)
    start_date = forms.DateField(
        widget=forms.TextInput(     
            attrs={'type': 'date'} 
        )
    )  
    end_date = forms.DateField(
        widget=forms.TextInput(     
            attrs={'type': 'date'} 
        )
    )  
    

class ProfileSelectForm(forms.Form):
    customer_id = forms.IntegerField(
        widget=forms.Select(choices=USER_CHOICES)
    ) 

class ToolTypeForm(forms.ModelForm):
    quantity = forms.IntegerField(max_value=15)
    class Meta:
         model = ToolType
         fields = ['type_name', 'description', 'image']

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
        fields =['address1', 'address2', 'city', 'state', 'image']
		
class ContactForm(forms.Form):
    contact_first_name = forms.CharField(required=True)
    contact_last_name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    content = forms.CharField(
        required=True,
        widget=forms.Textarea
    )