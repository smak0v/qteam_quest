from django import forms

from apps.quests.models import Quest, MetroStation, QuestImage


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


class QuestGalleryImageUploadForm(forms.ModelForm):
    """Class that implements quest`s gallery image upload form"""

    class Meta:
        model = QuestImage
        exclude = [
            'uploading_timespan',
            'quest',
        ]
