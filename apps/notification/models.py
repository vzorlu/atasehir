from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class NotificationSettings(models.Model):
    whatsapp = models.BooleanField(default=False)  # WhatsApp bildirimi
    mail = models.BooleanField(default=False)  # E-posta bildirimi
    sms = models.BooleanField(default=False)  # SMS bildirimi
    push = models.BooleanField(default=False)  # Push bildirimi
    notification = models.OneToOneField('Notifications', on_delete=models.CASCADE, related_name='notification_settings', null=True, blank=True)

class MailSettings(models.Model):
    smtp_server = models.CharField(max_length=255)
    smtp_port = models.IntegerField()
    smtp_user = models.CharField(max_length=255)
    smtp_password = models.CharField(max_length=255)
    notification = models.OneToOneField('Notifications', on_delete=models.CASCADE, related_name='mail_settings', null=True, blank=True)

class SmsSettings(models.Model):
    netgsm_user = models.CharField(max_length=255)
    netgsm_password = models.CharField(max_length=255)
    netgsm_header = models.CharField(max_length=255)
    notification = models.OneToOneField('Notifications', on_delete=models.CASCADE, related_name='sms_settings', null=True, blank=True)

class WhatsappSettings(models.Model):
    facebook_app_id = models.CharField(max_length=255)
    facebook_app_secret = models.CharField(max_length=255)
    facebook_access_token = models.CharField(max_length=255)
    notification = models.OneToOneField('Notifications', on_delete=models.CASCADE, related_name='whatsapp_settings', null=True, blank=True)

class Notifications(models.Model):
    NOTIFICATION_TYPES = [
        ('INFO', 'Information'),
        ('WARNING', 'Warning'),
        ('ERROR', 'Error'),
    ]

    title = models.CharField(max_length=255)  # Başlık
    type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)  # Bildirim türü
    is_notification = models.BooleanField(default=True)  # Bildirim aktif mi?
    customer = models.ForeignKey(
        'customer.Customer',
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='notification_notifications'  # Benzersiz related_name
    )

    def __str__(self):
        return self.title

    def whatsapp(self):
        return self.notification_settings.whatsapp

    def mail(self):
        return self.notification_settings.mail

    def sms(self):
        return self.notification_settings.sms

    def push(self):
        return self.notification_settings.push
