from django import forms
from app.models import Event, Location


class EventForm(forms.ModelForm):  
    class Meta:
        model = Event
        fields = ('event_type')


    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['event_type'].empty_label = "Select"
        self.fields['event_type'].required = True
