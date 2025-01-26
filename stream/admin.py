from django.contrib import admin
from .models import Detection, StreamImage


@admin.register(Detection)
class DetectionAdmin(admin.ModelAdmin):
    list_display = ("id", "image", "class_name", "x_min", "y_min", "x_max", "y_max", "confidence", "timestamp")
    list_filter = ("class_name", "timestamp")
    search_fields = ("class_name", "image__id")
    ordering = ("-timestamp",)


@admin.register(StreamImage)
class StreamImageAdmin(admin.ModelAdmin):
    list_display = ("id", "image", "timestamp")
    ordering = ("-timestamp",)
