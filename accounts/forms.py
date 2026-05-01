"""
accounts/forms.py
Registration form that also creates a UserProfile automatically.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


class RegistrationForm(UserCreationForm):
    """Extended registration form with email, first/last name."""

    email      = forms.EmailField(required=True, help_text='A valid email address is required.')
    first_name = forms.CharField(max_length=50, required=True)
    last_name  = forms.CharField(max_length=50, required=True)

    class Meta:
        model  = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to every field
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already registered.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email      = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name  = self.cleaned_data['last_name']
        if commit:
            user.save()
            # UserProfile is created by the post_save signal; just set role
            UserProfile.objects.get_or_create(user=user, defaults={'role': 'user'})
        return user


class UserProfileForm(forms.ModelForm):
    """Let users update their profile image."""

    class Meta:
        model  = UserProfile
        fields = ('profile_image',)
        widgets = {
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
        }
