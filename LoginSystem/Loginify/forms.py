from django import forms
from .models import UserDetails

class SignupForm(forms.Form):
    username = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=50)
    password = forms.CharField(max_length=12)

    def __str__(self):
        return self.username + ' ' + self.email
        
        