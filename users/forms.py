from django import forms
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm, UserChangeForm as DjangoUserChangeForm

from users.models import User, GENDERS


class UserCreationForm(DjangoUserCreationForm):
    """Class that represents user creation form on admin part of the site"""

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'location',
            'gender',
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

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'location',
            'gender',
        ]
