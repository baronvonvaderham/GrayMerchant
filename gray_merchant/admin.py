from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _


from .models import User, UserProfile, Vendor, Owner, Employee, UserAddress


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class UserAddressInLine(admin.StackedInline):
    model = UserAddress
    can_delete = False


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    inlines = (UserProfileInline, UserAddressInLine)


admin.site.register(Vendor)
admin.site.register(Owner)
admin.site.register(Employee)
