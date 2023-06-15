from .models import Customer
from django import forms
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        max_length=100,
        required=True,
        help_text='Enter Email Address',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
    )
    first_name = forms.CharField(
        max_length=100,
        required=True,
        help_text='Enter First Name',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
    )
    last_name = forms.CharField(
        max_length=100,
        required=True,
        help_text='Enter Last Name',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
    )
    password1 = forms.CharField(
        help_text='Enter Password',
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
    )
    password2 = forms.CharField(
        required=True,
        help_text='Enter Password Again',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password Again'}),
    )
    birth_day = forms.DateField(
        required=True,
        help_text='Enter BirthDay',
        widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Birthday'})
    )
    country = forms.CharField(
        required=True,
        help_text='Enter Country',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'})
    )
    region = forms.CharField(
        required=True,
        help_text='Enter Region',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Region'})
    )
    city = forms.CharField(
        required=True,
        help_text='Enter City',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'})
    )
    street_address = forms.CharField(
        required=True,
        help_text='Enter Street Address',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street Address'})
    )
    postal_code = forms.CharField(
        required=True,
        help_text='Enter Postal Code',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal Code'})
    )
    province = forms.CharField(
        required=True,
        help_text='Enter Province',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Province'})
    )

    class Meta:
        model = Customer
        fields = [
             'email', 'first_name', 'last_name', 'password1', 'password2', 'birth_day',
            'country', 'region', 'city', 'street_address', 'postal_code', 'province'
        ]
