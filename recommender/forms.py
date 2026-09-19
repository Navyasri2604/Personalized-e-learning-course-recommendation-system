from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'full_name')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('full_name', 'email', 'interests', 'skills', 'career_goal')
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'interests': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'e.g. AI, Web Development, Cloud Computing'}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'e.g. Python, Django, JavaScript'}),
            'career_goal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. AI Engineer, Full Stack Developer'}),
        }
