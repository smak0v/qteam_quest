from django.contrib import admin

from apps.coupons.models import Coupon


class CouponAdmin(admin.ModelAdmin):
    """Class that represents admin part of the coupon"""

    ordering = [
        'start_date',
        'end_date',
        'units',
        'type',
        'user',
    ]
    list_display = [
        'code',
        'start_date',
        'end_date',
        'discount',
        'units',
        'type',
        'user',
    ]
    search_fields = [
        'code',
        'start_date',
        'end_date',
        'discount',
        'units',
        'type',
        'user',
    ]
    list_per_page = 50


admin.site.register(Coupon, CouponAdmin)
