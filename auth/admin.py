from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "customer",
        "is_verified",
        "created_at",
    )

admin.site.register(Profile, ProfileAdmin)
