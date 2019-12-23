from django.shortcuts import render, redirect
from django.utils.datetime_safe import datetime
from django.views import View

from apps.coupons.forms import CouponForm
from apps.coupons.models import Coupon


class CouponsListView(View):
    """Class that implements coupons list view"""

    template_name = 'coupons/list.html'

    def get(self, request):
        active_coupons = Coupon.objects.filter(end_date__gte=datetime.now())
        not_active_coupons = Coupon.objects.filter(end_date__lt=datetime.now())
        context = {
            'title': 'Купоны',
            'active_coupons': active_coupons,
            'not_active_coupons': not_active_coupons,
        }
        return render(request=request, template_name=self.template_name, context=context)


def create_coupon_view(request):
    """Function that implements coupon create view"""

    template_name = 'coupons/create.html'
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='coupons:list')
        else:
            context = {
                'title': 'Создание купона',
                'form': form,
                'errors': form.errors,
            }
            return render(request=request, template_name='coupons/create.html', context=context)
    else:
        form = CouponForm()
        context = {
            'title': 'Создание купона',
            'form': form,
        }
        return render(request=request, template_name=template_name, context=context)


def edit_coupon_view(request, pk):
    """Function that implements coupon edit view"""

    template_name = 'coupons/edit.html'
    coupon = Coupon.objects.get(pk=pk)
    if request.method == 'POST':
        form = CouponForm(request.POST, instance=coupon)
        if form.is_valid():
            form.save()
            return redirect(to='coupons:list')
        else:
            context = {
                'title': 'Редактирование купона',
                'form': form,
                'errors': form.errors,
            }
            return render(request=request, template_name='coupons/edit.html', context=context)
    else:
        form = CouponForm(instance=coupon)
        context = {
            'title': 'Редактирование купона',
            'form': form,
        }
        return render(request=request, template_name=template_name, context=context)


def delete_coupon_view(request, pk):
    """Function that implements coupon delete view"""

    coupon = Coupon.objects.get(pk=pk)
    coupon.delete()
    return redirect(to='coupons:list')
