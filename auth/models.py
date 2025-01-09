from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.apps import apps

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(
        'customer.Customer',
        on_delete=models.CASCADE,
        related_name='profiles'
    )

    def __str__(self):
        return self.user.username

    def get_customer(self):
        Customer = apps.get_model('customer', 'Customer')
        return Customer
