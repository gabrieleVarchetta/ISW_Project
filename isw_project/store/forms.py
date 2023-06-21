from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email


class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(
        validators=[validate_email],
        widget=forms.EmailInput())
    password = forms.CharField(
        max_length=200,
        widget=forms.PasswordInput(),
        validators=[validate_password]
    )
    username = forms.CharField(max_length=100)
    birth_day = forms.DateField(input_formats=['%d/%m/%Y', '%d/%m/%y'])
    country = forms.CharField(max_length=256)
    region = forms.CharField(max_length=256)
    city = forms.CharField(max_length=256)
    street_address = forms.CharField(max_length=256)
    postal_code = forms.CharField(max_length=256)
    province = forms.CharField(max_length=256)


class AddressForm(forms.Form):
    country = forms.CharField(max_length=100)
    region = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    street_address = forms.CharField(max_length=100)
    postal_code = forms.CharField(max_length=100)
    province = forms.CharField(max_length=100)
