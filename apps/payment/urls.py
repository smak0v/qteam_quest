from django.urls import path

from apps.payment.api_views import PaymentSaveView, YandexNotificationsView

payment_api_urls = (
    [
        path('save/', PaymentSaveView.as_view(), name='payment_save'),

        # Yandex webhooks
        path('yandex_notifications/', YandexNotificationsView.as_view(), name='yandex_notifications'),
    ], 'api:payment')
