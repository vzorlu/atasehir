from django.contrib import admin
from . import models
from .models import Sources

@admin.register(models.Models)
class ModelsAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'notes')
    search_fields = ('title', 'type')
    list_filter = ('type',)

@admin.register(models.Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('city', 'district', 'neighborhood', 'street')
    search_fields = ('city', 'district', 'neighborhood', 'street')

@admin.register(Sources)
class SourcesAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'url', 'type', 'status', 'has_transition_lines')
    search_fields = ('title', 'location')
    list_filter = ('type', 'status', 'is_mobile', 'is_record')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'location', 'url', 'type', 'addtype')
        }),
        ('Video Properties', {
            'fields': ('fps', 'resolution', 'width', 'height', 'codec', 'total_frames')
        }),
        ('Settings', {
            'fields': ('is_mobile', 'is_record', 'record_folder', 'status')
        }),
        ('Location Information', {
            'fields': ('inlocation',)
        }),
        ('Detection Areas', {
            'fields': ('polygons', 'polygons_label', 'polygons_color')
        }),
        ('Transition Lines', {
            'fields': ('transition_lines', 'crossing_direction'),
            'description': 'Define transition lines and their crossing directions'
        }),
    )
    readonly_fields = ('resolution', 'width', 'height', 'fps', 'codec', 'total_frames')

    def has_transition_lines(self, obj):
        return bool(obj.transition_lines)
    has_transition_lines.boolean = True
    has_transition_lines.short_description = 'Has Transition Lines'


@admin.register(models.Services)
class ServicesAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    filter_horizontal = ('models',)

@admin.register(models.Reports)
class ReportsAdmin(admin.ModelAdmin):
    list_display = ('title', 'level', 'status', 'status_changed_by')
    search_fields = ('title', 'level', 'status', 'status_changed_by__username')
    list_filter = ('level', 'status')
    filter_horizontal = ('assigned_to', 'departments')

    def save_model(self, request, obj, form, change):
        if 'status' in form.changed_data:
            obj.status_changed_by = request.user
        super().save_model(request, obj, form, change)