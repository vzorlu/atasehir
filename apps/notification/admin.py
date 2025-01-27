from django.contrib import admin
from django.contrib import messages
from .models import Notification, NotificationChannel


@admin.register(NotificationChannel)
class NotificationChannelAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("rule_name", "get_channels", "user", "department", "created_at", "severity", "read")
    list_filter = ("type", "read", "severity", "created_at", "department")
    filter_horizontal = ("channels",)
    search_fields = ("rule_name", "message", "class_field")
    ordering = ("-created_at",)

    def get_channels(self, obj):
        return ", ".join([channel.get_name_display() for channel in obj.channels.all()])

    get_channels.short_description = "Bildirim Kanalları"

    def save_model(self, request, obj, form, change):
        try:
            super().save_model(request, obj, form, change)
        except Exception as e:
            messages.error(request, f"Error saving notification: {str(e)}")
            return

    def save_related(self, request, form, formsets, change):
        try:
            super().save_related(request, form, formsets, change)
        except Exception as e:
            messages.error(request, f"Error saving notification settings: {str(e)}")
            return
