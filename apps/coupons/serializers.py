from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.coupons.models import Coupon
from users.models import User
from users.serializers import UserSerializer


class CouponSerializer(serializers.ModelSerializer):
    """Class that implements coupon model serializer"""

    class Meta:
        model = Coupon
        fields = '__all__'

    def validate(self, data):
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
                user = User.objects.get(id=data['user'].pk)
            except User.DoesNotExist:
                raise ValidationError({
                    'user': 'Must be a real user!',
                })
        return data


class CouponRetrieveSerializer(serializers.ModelSerializer):
    """Class that implements coupon retrieve serializer"""

    user = UserSerializer()

    class Meta:
        model = Coupon
        fields = '__all__'


class CouponUpdateSerializer(serializers.ModelSerializer):
    """Class that implements coupone update serializer"""

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
                user = User.objects.get(id=data['user'].pk)
            except User.DoesNotExist:
                raise ValidationError({
                    'user': 'Must be a real user!',
                })
        return data
