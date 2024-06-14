# forms.py

from django import forms
from .models import Workshop, WorkshopDateTime

class WorkshopBookingForm(forms.Form):
    date = forms.ChoiceField(choices=[], label="Date")
    time = forms.ChoiceField(choices=[], label="Time")

    def __init__(self, *args, **kwargs):
        workshop_id = kwargs.pop('workshop_id', None)
        super().__init__(*args, **kwargs)
        if workshop_id:
            workshop = Workshop.objects.get(id=workshop_id)
            self.fields['date'].choices = self.get_date_choices(workshop)
            self.fields['time'].choices = self.get_time_choices(workshop)

    def get_date_choices(self, workshop):
        dates = set(dt.date_time.date() for dt in workshop.dates_times.all())
        choices = [(date, date.strftime('%Y-%m-%d')) for date in dates]
        return choices

    def get_time_choices(self, workshop):
        times = set(dt.date_time.time() for dt in workshop.dates_times.all())
        choices = [(time, time.strftime('%H:%M')) for time in times]
        return choices
