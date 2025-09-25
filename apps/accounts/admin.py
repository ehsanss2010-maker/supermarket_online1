from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Address, UserProfile


class AddressInline(admin.TabularInline):
    model = Address
    extra = 1
    fields = ['title', 'province', 'city', 'address_line', 'is_default_shipping', 'is_default_billing']


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'phone', 'first_name', 'last_name', 'is_active', 'date_joined']
    list_filter = ['is_active', 'is_staff', 'is_superuser', 'date_joined']
    search_fields = ['username', 'email', 'phone', 'first_name', 'last_name']
    ordering = ['-date_joined']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'),
         {'fields': ('first_name', 'last_name', 'email', 'phone', 'national_id', 'date_of_birth', 'avatar')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Preferences'), {'fields': ('newsletter_subscription',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone', 'password1', 'password2'),
        }),
    )

    inlines = [UserProfileInline, AddressInline]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'city', 'province', 'is_default_shipping', 'is_default_billing']
    list_filter = ['province', 'city', 'is_default_shipping', 'is_default_billing']
    search_fields = ['user__username', 'user__email', 'city', 'province']
    raw_id_fields = ['user']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'gender', 'total_orders', 'total_spent']
    list_filter = ['gender', 'preferred_language']
    search_fields = ['user__username', 'user__email']
    raw_id_fields = ['user']