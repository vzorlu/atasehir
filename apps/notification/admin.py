from django.contrib import admin
from .models import Notifications, NotificationSettings, MailSettings, SmsSettings, WhatsappSettings

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

class NotificationsAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'is_notification', 'whatsapp', 'mail', 'sms', 'push')
    list_filter = ('type', 'is_notification', 'notification_settings__whatsapp', 'notification_settings__mail', 'notification_settings__sms', 'notification_settings__push')
    inlines = [NotificationSettingsInline, MailSettingsInline, SmsSettingsInline, WhatsappSettingsInline]

    def whatsapp(self, obj):
        return obj.notification_settings.whatsapp

    def mail(self, obj):
        return obj.notification_settings.mail

    def sms(self, obj):
        return obj.notification_settings.sms

    def push(self, obj):
        return obj.notification_settings.push

admin.site.register(Notifications, NotificationsAdmin)
