from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm, UsernameField,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation
from .models import Customer

class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Enter your password'}), required=True)
    password2 = forms.CharField(label='Repeat Password (again)', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Enter your repeat password'}), required=True)
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Enter your Email'}), required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {'email': 'Email'}
        widgets = {'username': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter your Username'})}
        

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True, 'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(label=('Password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class': 'form-control', 'placeholder': 'Password'}))
    
class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=('Old Password'),strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class': 'form-control', 'placeholder': 'Old Password'}))
    new_password1 = forms.CharField(label=('New Password'),strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class': 'form-control', 'placeholder': 'New Password'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=('Confirm Password'),strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class': 'form-control', 'placeholder': 'Confirm Password'}))
    
    
class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=('Email'), max_length=254, widget=forms.EmailInput(attrs={'autocomplete':'email', 'class': 'form-control', 'placeholder': 'Email'}))


class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=('New Password'),strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class': 'form-control', 'placeholder': 'New Password'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=('Confirm Password'),strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class': 'form-control', 'placeholder': 'Confirm Password'}))


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'locality', 'city', 'state', 'zipcode']
        widgets = {
                'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Name'}),
                'locality': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Locality'}),
                'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'City'}),
                'state': forms.Select(attrs={'class': 'form-control'}),
                'zipcode': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'Zipcode'}),
                   }
