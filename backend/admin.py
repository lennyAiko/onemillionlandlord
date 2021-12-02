from django.contrib import admin
from .models import *


# Register your models here.

class ClientAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email')
    list_filter = ('date_created',)
    search_fields = ('username', 'first_name', 'last_name', 'phone')
    raw_id_fields = ("user",)


class PropertyAdmin(admin.ModelAdmin):
    list_filter = ('date_created',)
    search_fields = ('name', 'location')


class OrderAdmin(admin.ModelAdmin):
    raw_id_fields = ("client", "property")


admin.site.register(Client, ClientAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Staff)
admin.site.register(TenantOrder)
admin.site.register(Tenant)