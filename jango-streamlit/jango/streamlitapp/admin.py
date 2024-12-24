from django.contrib import admin
from .models import UploadedFile, UserData

# Register your models here.
admin.site.register(UploadedFile)
admin.site.register(UserData)
