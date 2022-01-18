from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import PasswordInput, EmailField

from dart_fss.errors import APIKeyError
from dart_fss import set_api_key
from django.core.exceptions import ValidationError
from user.validators import RegisteredEmailValidator, APIKeyValidator

class LoginForm(AuthenticationForm):
    username = EmailField(widget=forms.EmailInput(attrs={'autofocus': True}))


class SignUpForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('name', 'email', 'api_key')
        widgets= {
            'api_key': PasswordInput
        }
    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        api_key_validator = APIKeyValidator()
        api_key_validator(cleaned_data.get('api_key'))


class VerificationEmailForm(forms.Form):
    email = EmailField(widget=forms.EmailInput(attrs={'autofocus': True}), validators=(EmailField.default_validators + [RegisteredEmailValidator()]))
   
