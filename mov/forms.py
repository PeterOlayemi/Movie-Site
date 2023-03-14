from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import *

class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
  
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content']
