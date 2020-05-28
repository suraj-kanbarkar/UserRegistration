from django.core import validators
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# class NewUser(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = '__all__'


class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
