from django.urls import path

from apps.payment.api_views import PaymentSuccessView, YandexNotificationsView, PaymentErrorsView

payment_api_urls = (
    [
        path('success/', PaymentSuccessView.as_view(), name='payment_success'),
        path('error/', PaymentErrorsView.as_view(), name='payment_error'),

        # Yandex webhooks
        path('yandex_notifications/', YandexNotificationsView.as_view(), name='yandex_notifications'),
    ], 'api:payment')
