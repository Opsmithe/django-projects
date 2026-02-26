from django.contrib import admin
from .models import Names

# Register your models here.
# @admin.register() is a decorator that does the same as admin.site.register
class NamesAdmin(admin.ModelAdmin):
    list_display = ("firstname", "lastname", "city", "location", "date_joined", "date_started", "status")
    list_filter = ("firstname", "lastname", "date_joined")
    raw_id = ("firstname", "lastname")
    ordering = ("date_joined",)


admin.site.register(Names, NamesAdmin)

