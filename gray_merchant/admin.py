from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Vendor, Owner, Employee, Address


admin.site.register(User, UserAdmin)
admin.site.register(Vendor)
admin.site.register(Owner)
admin.site.register(Employee)
admin.site.register(Address)
