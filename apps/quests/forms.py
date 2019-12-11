from django import forms
from django.utils import timezone

from apps.quests.models import Game


class GameForm(forms.ModelForm):
    """Class that implements game model form"""

    timespan = forms.DateTimeField(
        initial=timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
    )

    class Meta:
        model = Game
        exclude = [
            'registration_available',
        ]
