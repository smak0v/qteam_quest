from django.conf import settings
from yandex_checkout import Configuration, Refund

from apps.games.models import GamePaymentRefund


def create_refund(game_payment, user, game):
    Configuration.account_id = settings.YANDEX_ACCOUNT_ID
    Configuration.secret_key = settings.YANDEX_SECRET_KEY
    refund = Refund.create({
        "amount": {
            "value": payment.amount.value,
            "currency": payment.amount.currency,
        },
        "payment_id": payment.id,
    })
    game_payment_refund = GamePaymentRefund.objects.create(
        identifier=refund.id,
        status='CANCELED' if refund.status == 'canceled' else 'SUCCEEDED',
        value=float(refund.amount.value),
        currency=refund.amount.currency,
        created_at=refund.created_at,
        payment=game_payment,
        user=user,
        game=game,
    )
    return game_payment_refund
