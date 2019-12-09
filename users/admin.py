from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site

from users.forms import UserCreationForm, UserChangeForm
from users.models import User, UserSubscription


class UserAdmin(DjangoUserAdmin):
    """Class that represents admin part of user"""

    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = [
        'phone',
        'is_active_phone',
        'username',
        'first_name',
        'last_name',
        'birthday_date',
        'gender',
        'location',
        'reliability',
        'active',
        'staff',
        'admin',
    ]
    ordering = [
        'phone',
        'is_active_phone',
        'username',
        'first_name',
        'last_name',
        'birthday_date',
        'gender',
        'location',
        'active',
        'staff',
        'admin',
    ]
    list_filter = [
        'is_active_phone',
        'gender',
        'active',
        'staff',
        'admin',
    ]
    search_fields = [
        'phone',
        'username',
        'first_name',
        'last_name',
        'birthday_date',
        'gender',
        'location',
    ]
    fieldsets = [
        [None, {'fields': ['phone', 'is_active_phone', 'phone_activation_code', 'username', 'password', 'active', ]}],
        ['Персональная информация', {'fields': ['first_name', 'last_name', 'about', ]}],
        ['Разрешения', {'fields': ['admin', 'staff']}],
        ['Другое', {'fields': ['location', 'gender', 'reliability', 'profile_image', ]}],
    ]
    filter_horizontal = []
    list_per_page = 50


class UserSubscriptionAdmin(admin.ModelAdmin):
    """Class that represents admin part of user subscription"""

    list_display = [
        'user',
        'subscriber',
    ]
    ordering = [
        'user',
        'subscriber',
    ]
    search_fields = [
        'user',
        'subscriber',
    ]
    list_per_page = 50


admin.site.unregister(Group)
admin.site.unregister(Site)

admin.site.register(User, UserAdmin)
admin.site.register(UserSubscription, UserSubscriptionAdmin)
