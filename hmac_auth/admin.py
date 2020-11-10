from django.contrib import admin

from hmac_auth.models import HMACGroup


@admin.register(HMACGroup)
class HMACGroupAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "permission_level")
    list_filter = ("permission_level",)
