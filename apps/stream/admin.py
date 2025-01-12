from django.contrib import admin
from .models import StreamImage, Detection

@admin.register(StreamImage)
class StreamImageAdmin(admin.ModelAdmin):
    list_display = ('__all__', 'processed', 'timestamp')
    list_filter = ('processed', 'timestamp')
    readonly_fields = ('timestamp', 'device')
    ordering = ('-timestamp',)

@admin.register(Detection)
class DetectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'class_name', 'x_coord', 'y_coord', 'confidence', 'timestamp')
    list_filter = ('class_name', 'timestamp')
    search_fields = ('class_name', 'image__id')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)
