from django import forms
from .models import StopEvent

class StopEventForm(forms.ModelForm):
    class Meta:
        model = StopEvent
        fields = [
            "trip",
            "stop",
            "arrival_time",
            "departure_time",
            "delay_seconds",
        ]
        widgets = {
            "arrival_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "departure_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }
