from django.core.validators import MinValueValidator
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.coupons.models import Coupon
from apps.games.models import Game
from users.models import User
from users.serializers import UserSerializer


class CouponSerializer(serializers.ModelSerializer):
    """Class that implements coupon model serializer"""

    class Meta:
        model = Coupon
        fields = '__all__'

    def validate(self, data):
        return validate_data(data)


class CouponRetrieveSerializer(serializers.ModelSerializer):
    """Class that implements coupon retrieve serializer"""

    user = UserSerializer()

    class Meta:
        model = Coupon
        fields = '__all__'


class CouponUpdateSerializer(serializers.ModelSerializer):
    """Class that implements coupon update serializer"""

    class Meta:
        model = Coupon
        fields = '__all__'
        extra_kwargs = {
            'code': {'required': False, },
            'start_date': {'required': False, },
            'end_date': {'required': False, },
            'discount': {'required': False, },
            'units': {'required': False, },
            'type': {'required': False, },
            'user': {'required': False, },
        }

    def validate(self, data):
        return validate_data(data)


class CouponCheckSerializer(serializers.Serializer):
    """Class that implements coupon check serializer"""

    code = serializers.CharField(
        max_length=10,
    )
    game_id = serializers.IntegerField(
        validators=[
            MinValueValidator(1),
        ]
    )

    def validate(self, data):
        try:
            coupon = Coupon.objects.get(code=data['code'])
        except Coupon.DoesNotExist:
            raise serializers.ValidationError({
                'code': 'Coupon with this code does not exist!',
            })
        try:
            game = Game.objects.get(pk=data['game_id'])
        except Game.DoesNotExist:
            raise serializers.ValidationError({
                'game_id': 'Game with this id does not exist!',
            })
        now_date = timezone.datetime.now().date()
        if now_date < coupon.start_date or now_date > coupon.end_date:
            raise serializers.ValidationError({
                'date': 'Coupon still / not valid!',
            })
        return data


def validate_data(data):
    if data['end_date'] < data['start_date']:
        raise ValidationError({
            'end_date': 'End date can`t be less than start_date!',
        })
    if data['type'] == 'GENERAL' and data['user']:
        raise ValidationError({
            'user': 'Must be NULL for GENERAL type of coupon!',
        })
    if data['type'] == 'INDIVIDUAL' and data['user'] is None:
        raise ValidationError({
            'user': 'User cant`t be NULL for INDIVIDUAL type of coupon!',
        })
    if data['type'] == 'INDIVIDUAL' and data['user']:
        try:
            User.objects.get(id=data['user'].pk)
        except User.DoesNotExist:
            raise ValidationError({
                'user': 'Must be a real user!',
            })
    return data
