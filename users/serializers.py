from drf_extra_fields.fields import Base64ImageField
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

from korobka_games.settings import ROOT_URL
from users.models import User, GENDERS, POSITIONS, UserSubscription, UserAuthToken, UserChangePhone, \
    UserChangePhoneConfirm


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
            'username',
            'first_name',
            'last_name',
            'email',
            'location',
            'gender',
            'nationality',
            'favourite_position',
            'active',
            'staff',
            'admin',
            'phone',
            'is_active_phone',
            'reliability',
            'profile_image',
        ]


class UserAuthTokenSerializer(serializers.ModelSerializer):
    """Class that implements user auth token serializer"""

    token = serializers.CharField(
        max_length=255,
        required=True
    )

    class Meta:
        model = UserAuthToken
        fields = [
            'token',
        ]


class UserChangePhoneNumberSerializer(serializers.ModelSerializer):
    """Class that implements user change phone number serializer"""

    phone = serializers.CharField(
        max_length=15,
        required=True
    )

    class Meta:
        model = UserChangePhone
        fields = [
            'phone',
        ]


class UserChangePhoneNumberConfirmSerializer(serializers.ModelSerializer):
    """Class that implements user change phone number confirm serializer"""

    sms_code = serializers.CharField(
        max_length=5,
        required=True
    )

    class Meta:
        model = UserChangePhoneConfirm
        fields = [
            'sms_code',
        ]


class UserRegisterSerializer(RegisterSerializer):
    """Class that implements user register serializer"""

    username = serializers.CharField(
        required=True,
    )
    password1 = serializers.CharField(
        write_only=True,
    )
    first_name = serializers.CharField(
        required=True,
    )
    last_name = serializers.CharField(
        required=True,
    )
    email = serializers.EmailField(
        required=True,
    )
    location = serializers.CharField(
        required=False,
    )
    gender = serializers.ChoiceField(
        required=False,
        choices=GENDERS,
    )
    nationality = serializers.CharField(
        required=False,
    )
    favourite_position = serializers.ChoiceField(
        required=False,
        choices=POSITIONS,
    )
    phone = serializers.CharField(
        required=False,
    )
    is_active_phone = serializers.BooleanField(
        required=False,
        default=False,
    )

    def get_cleaned_data(self):
        super(UserRegisterSerializer, self).get_cleaned_data()
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'email': self.validated_data.get('email', ''),
            'location': self.validated_data.get('location', ''),
            'gender': self.validated_data.get('gender', 'NOT_SET'),
            'nationality': self.validated_data.get('nationality', ''),
            'favourite_position': self.validated_data.get('favourite_position', 'NOT_SET'),
            'phone': self.validated_data.get('phone', ''),
            'is_active_phone': self.validated_data.get('is_active_phone', False),
        }

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


IMAGE_EXTENSIONS = [
    ('.jpg', 'JPG, JPEG'),
    ('.png', 'PNG'),
]


class UpdateUserProfileSerializer(serializers.Serializer):
    """Class that represents update user profile serializer"""

    username = serializers.CharField(
        required=False,
    )
    first_name = serializers.CharField(
        required=False,
    )
    last_name = serializers.CharField(
        required=False,
    )
    email = serializers.EmailField(
        required=False,
    )
    location = serializers.CharField(
        required=False,
    )
    gender = serializers.ChoiceField(
        required=False,
        choices=GENDERS,
    )
    nationality = serializers.CharField(
        required=False,
    )
    favourite_position = serializers.ChoiceField(
        required=False,
        choices=POSITIONS,
    )
    profile_image = Base64ImageField(
        required=False,
    )

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


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

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class UserSubscriptionCreateSerializer(serializers.ModelSerializer):
    """Class that represents user subscription create serializer"""

    class Meta:
        model = UserSubscription
        fields = '__all__'

    def validate(self, data):
        try:
            user_subscription = UserSubscription.objects.get(user=data['user'], subscriber=data['subscriber'])
            raise serializers.ValidationError('Subscription already exists!')
        except UserSubscription.DoesNotExist:
            if data['user'] == data['subscriber']:
                raise serializers.ValidationError('Unable to subscribe to myself!')
            return data


class UserSubscriptionSerializer(serializers.ModelSerializer):
    """Class that represents user subscription serializer"""

    user = UserSerializer()
    subscriber = UserSerializer()

    class Meta:
        model = UserSubscription
        fields = '__all__'
