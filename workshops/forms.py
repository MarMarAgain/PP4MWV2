from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

        widgets = {
            'rating': forms.RadioSelect(choices=Review.RATING_CHOICES),  # Display rating as radio buttons
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Leave a comment (optional)'}),
        }

        labels = {
            'rating': 'Rating',
            'comment': 'Your Comment',
        }
