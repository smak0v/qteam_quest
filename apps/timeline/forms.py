from django import forms

from apps.timeline.models import TimelineBlock


class TimelineBlockForm(forms.ModelForm):
    """Class that implements timeline block model form"""

    class Meta:
        model = TimelineBlock
        exclude = [
            'timespan',
            'creator',
        ]

    def clean(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('type') == 'GAME_MESSAGE' and not cleaned_data.get('game'):
            self.add_error('game', 'Выберите игру для отправки сообщения!')
        return cleaned_data
