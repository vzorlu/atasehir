from django.contrib import admin
from django.contrib import messages
from .models import Notification, MailSettings, SmsSettings, WhatsappSettings


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


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "user", "department", "created_at", "read", "severity")
    list_filter = ("type", "read", "created_at", "department", "severity")
    search_fields = ("title", "message", "class_field")
    inlines = [MailSettingsInline, SmsSettingsInline, WhatsappSettingsInline]
    ordering = ("-created_at",)

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
