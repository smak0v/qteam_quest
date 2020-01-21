from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.coupons.models import Coupon
from apps.coupons.serializers import CouponSerializer, CouponRetrieveSerializer, CouponUpdateSerializer, \
    CouponCheckSerializer
from apps.games.models import Game
from apps.permissions import IsStaffUser
from apps.teams.models import TemporaryReserve


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

    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, *argc, **kwargs):
        user = self.request.user
        serializer = CouponCheckSerializer(data=self.request.data)
        if serializer.is_valid():
            reserved_places_count = TemporaryReserve.objects.filter(user=user.pk,
                                                                    game=serializer.validated_data['game_id']).count()
            if reserved_places_count == 0:
                return Response({
                    'error': 'You have no reserved seats for this game or payment time exceeded 5 minutes. Try again!',
                }, status=status.HTTP_400_BAD_REQUEST)
            coupon = Coupon.objects.get(code=serializer.validated_data.get('code'))
            game = Game.objects.get(pk=serializer.validated_data['game_id'])
            if coupon.type == 'INDIVIDUAL':
                if coupon.user != user:
                    return Response({
                        'error': 'Invalid user for this INDIVIDUAL coupon!',
                    }, status=status.HTTP_400_BAD_REQUEST)
                summa = self.apply_individual_discount(coupon, game, reserved_places_count)
            else:
                summa = self.apply_general_discount(coupon, game, reserved_places_count)
            response = {
                'summa': summa,
                'discount': coupon.discount,
                'units': coupon.units,
                'type': coupon.type,
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def apply_general_discount(coupon, game, reserved_places_count):
        summa = game.price * reserved_places_count
        if coupon.units == 'RUB':
            summa -= coupon.discount
        elif coupon.units == 'PERCENT':
            summa -= (game.price * coupon.discount) / 100
        return round(summa, 2)

    @staticmethod
    def apply_individual_discount(coupon, game, reserved_places_count):
        summa = game.price * reserved_places_count
        if coupon.units == 'RUB':
            summa -= coupon.discount
        elif coupon.units == 'PERCENT':
            summa -= (game.price * coupon.discount) / 100
        return round(summa, 2)
