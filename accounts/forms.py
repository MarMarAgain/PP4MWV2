from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['school_details', 'students_info']
        widgets = {
            'school_details': forms.Textarea(attrs={'placeholder': "Please enter your school's details here"}),
            'students_info': forms.Textarea(attrs={
                'placeholder': 'Please enter the cycle and level you primarily teach here. You can also add any other information you think may be relevant.'}),
        }