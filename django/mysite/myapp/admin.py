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

admin.site.register(MenuItem)

