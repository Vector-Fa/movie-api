from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Follow, FavoriteMovie, VerifyCode


admin.site.register([Follow, FavoriteMovie, VerifyCode])


class UserAdmin(BaseUserAdmin):
    list_display = ["username", "email", "is_admin"]
    list_filter = ["is_admin", "is_active"]

    # Specify the fieldsets for your custom User model
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('bio', 'photo')}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
    )


admin.site.register(User, UserAdmin)

