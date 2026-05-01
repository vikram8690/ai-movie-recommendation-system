"""reviews/forms.py — Review submission form with star rating."""

from django import forms
from .models import Review


STAR_CHOICES = [(i, f'{i} Star{"s" if i > 1 else ""}') for i in range(1, 6)]


class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=STAR_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'star-radio'}),
        label='Your Rating',
    )

    class Meta:
        model   = Review
        fields  = ['rating', 'review_text']
        widgets = {
            'review_text': forms.Textarea(attrs={
                'class':       'form-control',
                'rows':        5,
                'placeholder': 'Share your thoughts about this movie...',
            }),
        }
        labels = {
            'review_text': 'Your Review',
        }

    def clean_rating(self):
        rating = int(self.cleaned_data.get('rating', 0))
        if not (1 <= rating <= 5):
            raise forms.ValidationError('Rating must be between 1 and 5.')
        return rating
