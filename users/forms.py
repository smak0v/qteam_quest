from django import forms
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm, UserChangeForm as DjangoUserChangeForm

from users.models import User, GENDERS, POSITIONS


class UserCreationForm(DjangoUserCreationForm):
    """Class that represents user creation form on admin part of the site"""

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'location',
            'gender',
            'nationality',
            'favourite_position',
        ]


class UserChangeForm(DjangoUserChangeForm):
    """Class that represents user change form on admin part of the site"""

    location = forms.CharField(
        required=False,
    )
    gender = forms.ChoiceField(
        choices=GENDERS,
        required=False,
    )
    nationality = forms.CharField(
        required=False,
    )
    favourite_position = forms.ChoiceField(
        choices=POSITIONS,
        required=False,
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'location',
            'gender',
            'nationality',
            'favourite_position',
        ]
