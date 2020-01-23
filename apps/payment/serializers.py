from rest_framework import serializers

from apps.games.models import Game, GamePayment


class PaymentSuccessSerializer(serializers.Serializer):
    """Class that implements payment success serializer"""

    game_id = serializers.IntegerField()
    payment_id = serializers.CharField(
        max_length=255,
    )

    def validate(self, data):
        try:
            game = Game.objects.get(pk=data['game_id'])
        except Game.DoesNotExist:
            raise serializers.ValidationError({
                'game_id': f'Game with id {data["game_id"]} does not exist!',
            })
        try:
            game_payment = GamePayment.objects.get(identifier=data['payment_id'])
        except GamePayment.DoesNotExist:
            raise serializers.ValidationError({
                'payment_id': f'Payment with id {data["payment_id"]} does not exist!',
            })
        return data


class PaymentErrorSerializer(serializers.Serializer):
    """Class that implements payment error serializer"""

    error = serializers.CharField(
        max_length=255,
    )
    payment_id = serializers.CharField(
        max_length=255,
    )

    def validate(self, data):
        try:
            game_payment = GamePayment.objects.get(identifier=data['payment_id'])
        except GamePayment.DoesNotExist:
            raise serializers.ValidationError({
                'payment_id': f'Payment with id {data["payment_id"]} does not exist!',
            })
        return data
