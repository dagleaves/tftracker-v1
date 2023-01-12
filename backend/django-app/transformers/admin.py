from ast import Sub
from django.contrib import admin
from users.models import UserAccount
from transformers.models import Transformer, Toyline, Subline

class UserAccountAdmin(admin.ModelAdmin):
    pass

class TransformerAdmin(admin.ModelAdmin):
    readonly_fields = ['id',]

class ToylineAdmin(admin.ModelAdmin):
    pass

class SublineAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserAccount, UserAccountAdmin)
admin.site.register(Transformer, TransformerAdmin)
admin.site.register(Toyline, ToylineAdmin)
admin.site.register(Subline, SublineAdmin)