from django.urls import path

from apps.payment.api_views import PaymentSuccessView

payment_api_urls = (
    [
        path('success/', PaymentSuccessView.as_view(), name='payment_success'),
    ], 'api:payment')
