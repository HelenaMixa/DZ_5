from django.contrib import admin

from .models import Dancer, Coach, Club

admin.site.register(Dancer),
admin.site.register(Coach),
admin.site.register(Club),


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')

