from django import forms
from .models import Review,WorkshopDateTime


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


class WorkshopBookingForm(forms.Form):
    event = forms.ModelChoiceField(
        queryset=WorkshopDateTime.objects.none(),
        widget=forms.Select
    )

    def __init__(self, *args, **kwargs):
        workshop_id = kwargs.pop('workshop_id')
        super().__init__(*args, **kwargs)
        self.fields['event'].queryset = WorkshopDateTime.objects.filter(workshop_id=workshop_id)

