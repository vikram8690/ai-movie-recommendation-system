"""movies/forms.py — Form for creating and editing movies."""

from django import forms
from .models import Movie


class MovieForm(forms.ModelForm):
    class Meta:
        model  = Movie
        fields = ['title', 'description', 'genre', 'release_year', 'director', 'actors', 'poster']
        widgets = {
            'title':        forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Movie title'}),
            'description':  forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Short synopsis...'}),
            'genre':        forms.Select(attrs={'class': 'form-select'}),
            'release_year': forms.NumberInput(attrs={'class': 'form-control', 'min': 1900, 'max': 2030}),
            'director':     forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Director name'}),
            'actors':       forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Actor 1, Actor 2, Actor 3'}),
            'poster':       forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_release_year(self):
        year = self.cleaned_data.get('release_year')
        if year and (year < 1888 or year > 2030):
            raise forms.ValidationError("Please enter a valid release year between 1888 and 2030.")
        return year
