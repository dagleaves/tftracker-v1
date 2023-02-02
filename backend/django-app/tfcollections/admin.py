from django.contrib import admin
from .models import Collection, CollectionItem


class CollectionAdmin(admin.ModelAdmin):
    pass


class CollectionItemAdmin(admin.ModelAdmin):
    pass


admin.site.register(Collection, CollectionAdmin)
admin.site.register(CollectionItem, CollectionItemAdmin)
