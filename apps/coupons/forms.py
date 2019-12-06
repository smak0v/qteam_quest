from django import forms

from apps.coupons.models import Coupon


class CouponForm(forms.ModelForm):
    """Class that implements coupon model form"""

    class Meta:
        model = Coupon
        fields = '__all__'
