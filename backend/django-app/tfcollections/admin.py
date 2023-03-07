from django.contrib import admin
from .models import Collection, CollectionItem


class CollectionItemInline(admin.TabularInline):
    model = CollectionItem
    extra = 0


class CollectionAdmin(admin.ModelAdmin):
    model = Collection
    inlines = [
        CollectionItemInline
    ]


class CollectionItemAdmin(admin.ModelAdmin):
    pass


admin.site.register(Collection, CollectionAdmin)
admin.site.register(CollectionItem, CollectionItemAdmin)
