from django import forms
from .models import Workshop, WorkshopDateTime

class WorkshopBookingForm(forms.ModelForm):
    class Meta:
        model = WorkshopDateTime
        fields = ['date_time']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        workshop_id = self.initial.get('workshop_id')
        if workshop_id:
            self.fields['date_time'].widget = forms.Select(choices=self.get_time_choices(workshop_id))
        else:
            self.fields['date_time'].widget = forms.Select(choices=[])

    def get_time_choices(self, workshop_id):
        workshop = Workshop.objects.get(id=workshop_id)
        date_times = workshop.dates_times.all()
        choices = [(dt.id, f"{dt.date_time.strftime('%Y-%m-%d %H:%M')}") for dt in date_times]
        return choices
