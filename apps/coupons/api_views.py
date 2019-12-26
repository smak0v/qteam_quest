from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.coupons.models import Coupon
from apps.coupons.serializers import CouponSerializer, CouponRetrieveSerializer, CouponUpdateSerializer, \
    CouponCheckSerializer
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
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            return CouponUpdateSerializer
        if self.request.method == 'DELETE':
            return CouponSerializer


class CouponCheckAPIView(APIView):
    """Class that implements check coupon API view"""

    def post(self, *argc, **kwargs):
        serializer = CouponCheckSerializer(data=self.request.data)
        if serializer.is_valid():
            coupon = Coupon.objects.get(code=serializer.validated_data.get('code'))
            response = {
                'discount': coupon.discount,
                'units': coupon.units,
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
