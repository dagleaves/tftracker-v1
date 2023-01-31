from django.contrib import admin
from .models import UserPreferences


class UserPreferencesAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserPreferences, UserPreferencesAdmin)
