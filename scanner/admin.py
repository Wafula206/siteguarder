from django.contrib import admin
from .models import ScanResult

@admin.register(ScanResult)
class ScanResultAdmin(admin.ModelAdmin):
    list_display = ('url', 'scan_time', 'is_https')
    search_fields = ('url',)
    list_filter = ('is_https', 'scan_time')