from django.contrib import admin
from . import models
from .models import MenuItem

# Register your models here.

admin.site.register(models.Member)
admin.site.register(models.Menu)

admin.site.register(models.Coupon)

admin.site.register(models.Promotion)

admin.site.register(models.Event)

admin.site.register(models.Review)

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'rating', 'image')
    fields = ('name', 'description', 'price', 'rating', 'image')

admin.site.register(MenuItem, MenuItemAdmin)
