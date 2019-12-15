from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from qteam_quest.settings import ROOT_URL
from users.models import User, GENDERS, UserSubscription

IMAGE_EXTENSIONS = [
    ('.jpg', 'JPG, JPEG'),
    ('.png', 'PNG'),
]


class UserSerializer(serializers.ModelSerializer):
    """Class that implements user serializer"""

    profile_image = serializers.SerializerMethodField()

    @staticmethod
    def get_profile_image(user):
        if not user.profile_image:
            return ROOT_URL + '/static/img/no_user.png'
        return ROOT_URL + user.profile_image.url

    class Meta:
        model = User
        fields = [
            'id',
            'phone',
            'is_active_phone',
            'username',
            'first_name',
            'last_name',
            'location',
            'gender',
            'active',
            'staff',
            'admin',
            'reliability',
            'profile_image',
            'about',
            'birthday_date',
        ]


class UserLoginSerializer(serializers.Serializer):
    """Class that implements user login serializer"""

    phone = serializers.CharField(
        required=True,
    )


class UserLoginConfirmSerializer(serializers.Serializer):
    """Class that implements user login confirm serializer"""

    phone = serializers.CharField(
        required=True,
    )
    sms_code = serializers.CharField(
        required=True,
    )


class UserAuthTokenSerializer(serializers.Serializer):
    """Class that implements user auth token serializer"""

    token = serializers.CharField(
        max_length=255,
        required=True
    )


class UserChangePhoneNumberSerializer(serializers.Serializer):
    """Class that implements user change phone number serializer"""

    phone = serializers.CharField(
        max_length=15,
        required=True
    )


class UserChangePhoneNumberConfirmSerializer(serializers.Serializer):
    """Class that implements user change phone number confirm serializer"""

    sms_code = serializers.CharField(
        max_length=5,
        required=True
    )


class UpdateUserProfileSerializer(serializers.Serializer):
    """Class that represents update user profile serializer"""

    phone = serializers.CharField(
        required=False,
    )
    username = serializers.CharField(
        required=False,
    )
    first_name = serializers.CharField(
        required=False,
    )
    last_name = serializers.CharField(
        required=False,
    )
    birthday_date = serializers.DateField(
        required=False,
    )
    gender = serializers.ChoiceField(
        required=False,
        choices=GENDERS,
    )
    location = serializers.CharField(
        required=False,
    )
    profile_image = Base64ImageField(
        required=False,
    )
    about = serializers.CharField(
        required=False,
    )


class UserSubscriptionCreateSerializer(serializers.ModelSerializer):
    """Class that represents user subscription create serializer"""

    class Meta:
        model = UserSubscription
        fields = '__all__'

    def validate(self, data):
        try:
            UserSubscription.objects.get(user=data['user'], subscriber=data['subscriber'])
            raise serializers.ValidationError({
                'error': 'Subscription already exists!',
            })
        except UserSubscription.DoesNotExist:
            if data['user'] == data['subscriber']:
                raise serializers.ValidationError({
                    'error': 'Unable to subscribe by yourself!',
                })
            return data


class UserSubscriptionSerializer(serializers.ModelSerializer):
    """Class that represents user subscription serializer"""

    user = UserSerializer()
    subscriber = UserSerializer()

    class Meta:
        model = UserSubscription
        fields = '__all__'


class UserChangePasswordSerializer(serializers.Serializer):
    """Class that represents user password change serializer"""

    old_password = serializers.CharField(
        required=True,
    )
    new_password_1 = serializers.CharField(
        required=True,
    )
    new_password_2 = serializers.CharField(
        required=True,
    )
