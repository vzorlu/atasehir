from django.contrib import admin
from .models import Notification, NotificationSettings, MailSettings, SmsSettings, WhatsappSettings


class NotificationSettingsInline(admin.StackedInline):
    model = NotificationSettings
    can_delete = False


class MailSettingsInline(admin.StackedInline):
    model = MailSettings
    can_delete = False


class SmsSettingsInline(admin.StackedInline):
    model = SmsSettings
    can_delete = False


class WhatsappSettingsInline(admin.StackedInline):
    model = WhatsappSettings
    can_delete = False


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "user", "created_at", "read")
    list_filter = ("type", "read", "created_at")
    search_fields = ("title", "message")
    inlines = [NotificationSettingsInline, MailSettingsInline, SmsSettingsInline, WhatsappSettingsInline]
    ordering = ("-created_at",)
