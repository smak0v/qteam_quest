from django import forms

from apps.quests.models import Quest, MetroStation


class QuestForm(forms.ModelForm):
    """Class that implements quests model form"""

    class Meta:
        model = Quest
        exclude = [
            'rating',
        ]


class QuestMetroStationForm(forms.ModelForm):
    """Class that implements quests metro station model form"""

    class Meta:
        model = MetroStation
        exclude = [
            'quest',
        ]
