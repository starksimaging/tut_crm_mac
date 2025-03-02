from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='', widget=forms.EmailInput(attrs={'class': 'form_control', 'placeholder': 'Email'}))
    first_name = forms.CharField(max_length=30, label='', widget=forms.TextInput(attrs={'class': 'form_control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, label='', widget=forms.TextInput(attrs={'class': 'form_control', 'placeholder': 'Last Name'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
           

        self.fields['username'].widget.attrs['class'] = 'form_control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'

        self.fields['password1'].widget.attrs['class'] = 'form_control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'

        self.fields['password2'].widget.attrs['class'] = 'form_control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'