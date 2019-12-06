from django.contrib.auth.decorators import login_required
from django.urls import path

from apps.coupons.api_views import CouponListCreateAPIView, CouponRetrieveUpdateDestroyAPIView
from apps.coupons.views import CouponsListView, create_coupon_view, edit_coupon_view, \
    delete_coupon_view

coupons_urls = (
    [
        path('', login_required(CouponsListView.as_view()), name='list'),
        path('create/', login_required(create_coupon_view), name='create'),
        path('edit/<int:pk>/', login_required(edit_coupon_view), name='edit'),
        path('delete/<int:pk>/', login_required(delete_coupon_view), name='delete'),
    ], 'coupons')

coupons_api_urls = (
    [
        path('', CouponListCreateAPIView.as_view(), name='coupons_list'),
        path('<int:pk>/', CouponRetrieveUpdateDestroyAPIView.as_view(), name='coupon_detail'),

    ], 'api:coupons')
