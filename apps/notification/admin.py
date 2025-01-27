from django.contrib import admin
from django.contrib import messages
from .models import Notification, NotificationChannel, MailSettings, SmsSettings, WhatsappSettings, PushNotification


@admin.register(NotificationChannel)
class NotificationChannelAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(MailSettings)
class MailSettingsAdmin(admin.ModelAdmin):
    list_display = ("notification", "smtp_host", "from_email", "enabled")
    list_filter = ("enabled",)
    search_fields = ("smtp_host", "from_email")


@admin.register(SmsSettings)
class SmsSettingsAdmin(admin.ModelAdmin):
    list_display = ("notification", "sender_name", "api_endpoint", "enabled")
    list_filter = ("enabled",)
    search_fields = ("sender_name", "api_endpoint")


@admin.register(WhatsappSettings)
class WhatsappSettingsAdmin(admin.ModelAdmin):
    list_display = ("notification", "wa_phone_number", "wa_api_endpoint", "enabled")
    list_filter = ("enabled",)
    search_fields = ("wa_phone_number", "wa_api_endpoint")


@admin.register(PushNotification)
class PushNotificationAdmin(admin.ModelAdmin):
    list_display = ("get_notification_name", "app_key", "device_token", "enabled")
    list_filter = ("enabled",)
    search_fields = ("app_key", "device_token")

    def get_notification_name(self, obj):
        return obj.notification.rule_name if obj.notification else "-"

    get_notification_name.short_description = "Notification"


class MailSettingsInline(admin.StackedInline):
    model = MailSettings
    can_delete = False
    extra = 1


class SmsSettingsInline(admin.StackedInline):
    model = SmsSettings
    can_delete = False
    extra = 1


class WhatsappSettingsInline(admin.StackedInline):
    model = WhatsappSettings
    can_delete = False
    extra = 1


class PushNotificationInline(admin.StackedInline):
    model = PushNotification
    can_delete = False
    extra = 1


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("rule_name", "get_channels", "user", "department", "created_at", "severity", "read")
    list_filter = ("type", "read", "severity", "created_at", "department")
    filter_horizontal = ("channels",)
    search_fields = ("rule_name", "message", "class_field")
    inlines = [MailSettingsInline, SmsSettingsInline, WhatsappSettingsInline, PushNotificationInline]
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
