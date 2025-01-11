from django.contrib import admin
from .models import StreamImage, Detection

@admin.register(StreamImage)
class StreamImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'timestamp', 'processed', 'image_preview')
    list_filter = ('processed', 'timestamp')
    search_fields = ('id',)
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)

    def image_preview(self, obj):
        return f'<img src="{obj.image.url}" width="100" />' if obj.image else ''
    image_preview.allow_tags = True
    image_preview.short_description = 'Preview'

@admin.register(Detection)
class DetectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'class_name', 'x_coord', 'y_coord', 'confidence', 'timestamp', 'deviceuuid')
    list_filter = ('class_name', 'timestamp')
    search_fields = ('class_name', 'image__id')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)
