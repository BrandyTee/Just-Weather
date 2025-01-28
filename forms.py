from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm

#Lets create the registration form
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control', 
        'placeholder': 'name@example.com',
        'style': 'background-color: #000; color: white; width: 100%; z-index: 1000;' }))
    
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'style': 'background-color: #000; color: white; width: 100%; z-index: 1000;' }))
    
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'style': 'background-color: #000; color: white; width: 100%; z-index: 1000;', }))
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['style'] = 'background-color: #000; color: white; width: 100%; z-index: 1000;'
        self.fields['username'].help_text = (
            "Username must be one word. And only contain words, digits and special charatcters"
        )
        
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['type'] = 'password'
        self.fields['password1'].widget.attrs['style'] = 'background-color: #000; color: white; width: 100%; z-index: 1000;'
        self.fields['password1'].help_text = (
            "Your password must be 6-20 characters long, contain letters and numbers, It must not contain spaces, and can't be too similar to other personal information"
        
        )
        
        
        
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['type'] = 'password'
        self.fields['password2'].widget.attrs['style'] = 'background-color: #000; color: white; width: 100%; z-index: 1000;'
        self.fields['password2'].help_text = (
            "Enter Password Again For Verication"
        )


