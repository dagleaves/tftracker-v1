from django.contrib import admin
from .models import UserAccount
from tfcollections.models import Collection


class CollectionsInline(admin.TabularInline):
    model = Collection
    extra = 0


class UserAccountAdmin(admin.ModelAdmin):
    model = UserAccount

    inlines = [
        CollectionsInline
    ]


admin.site.register(UserAccount, UserAccountAdmin)
