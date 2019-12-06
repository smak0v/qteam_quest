from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from apps.coupons.models import Coupon
from apps.coupons.serializers import CouponSerializer, CouponRetrieveSerializer, CouponUpdateSerializer
from apps.permissions import IsStaffUser


class CouponListCreateAPIView(ListCreateAPIView):
    """Class that implements coupon list, create API views"""

    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [
        IsStaffUser,
    ]


class CouponRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """Class that implements coupon retrieve, update, destroy API view"""

    queryset = Coupon.objects.all()
    permission_classes = [
        IsStaffUser,
    ]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CouponRetrieveSerializer
        if self.request.method == 'PUT' or self.request.method == 'PATHC':
            return CouponUpdateSerializer
        if self.request.method == 'DELETE':
            return CouponSerializer
