# admin.py

from django.contrib import admin
from .models import Device, License, DeviceData, DeviceReport, Notification
from django.contrib import messages
from django.conf import settings
from onesignal_sdk.client import Client

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'name', 'license_key', 'registered_on', 'mac_address')
    search_fields = ('device_id', 'name', 'mac_address')

@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    list_display = ('license_key', 'license_type', 'is_active', 'expiry_date', 'available_devices')
    search_fields = ('license_key',)

@admin.register(DeviceData)
class DeviceDataAdmin(admin.ModelAdmin):
    list_display = ('device', 'cpu_usage', 'memory_usage', 'disk_space', 'timestamp')
    search_fields = ('device__device_id',)

@admin.register(DeviceReport)
class DeviceReportAdmin(admin.ModelAdmin):
    list_display = ('mac_address', 'created_at')
    search_fields = ('mac_address',)

class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "title", "message", "image", "camera", "alertLevel", "category",
        "segment", "sent_at", "status"
    )  # Tüm alanları ekledik
    search_fields = ("title", "message", "camera", "alertLevel", "category")
    list_filter = ("alertLevel", "category", "status", "sent_at") # list_display alanlarını doğru isimlerle güncelledik
    actions = ["send_notification"]

    def send_notification(self, request, queryset):
        for notification in queryset:
            response = notification.send_push_notification()

            if response.get("errors"):
                self.message_user(request, f"Bildirim gönderim hatası: {response['errors']}", level=messages.ERROR)
            else:
                self.message_user(request, "Bildirim başarıyla gönderildi.", level=messages.SUCCESS)

    send_notification.short_description = "Seçili bildirimleri gönder"

admin.site.register(Notification, NotificationAdmin)
