from django import forms

from apps.venues.models import Venue, MetroStation


class VenueForm(forms.ModelForm):
    """Class that implements venue model form"""

    class Meta:
        model = Venue
        exclude = [
            'rating',
        ]


class VenueMetroStationForm(forms.ModelForm):
    """Class that implements venue metro station model form"""

    class Meta:
        model = MetroStation
        exclude = [
            'venue',
        ]
