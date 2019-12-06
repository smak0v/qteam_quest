from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from users.forms import UserCreationForm, UserChangeForm
from users.models import User, UserSubscription


class UserAdmin(DjangoUserAdmin):
    """Class that represents admin part of user"""

    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    ordering = [
        'username',
        'first_name',
        'last_name',
        'email',
        'active',
        'staff',
        'admin',
        'is_active_phone',
        'reliability',
    ]
    list_display = [
        'username',
        'first_name',
        'last_name',
        'email',
        'active',
        'staff',
        'admin',
        'phone',
        'is_active_phone',
        'reliability',
    ]
    list_filter = [
        'gender',
        'nationality',
        'favourite_position',
        'active',
        'staff',
        'admin',
        'is_active_phone',
    ]
    search_fields = [
        'username',
        'first_name',
        'last_name',
        'email',
        'location',
        'nationality',
        'phone',
    ]
    fieldsets = [
        [None, {'fields': ['username', 'email', 'password', 'active', ]}],
        ['Персональная информация', {'fields': ['first_name', 'last_name', ]}],
        ['Разрешения', {'fields': ['admin', 'staff']}],
        ['Другое', {'fields': ['location', 'gender', 'nationality', 'favourite_position', 'phone', 'is_active_phone',
                               'phone_activation_code', 'reliability', 'profile_image', ]}],
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


admin.site.register(User, UserAdmin)
admin.site.register(UserSubscription, UserSubscriptionAdmin)
