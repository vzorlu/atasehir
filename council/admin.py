from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export.formats import base_formats
from .models import Way, Department
from .resources import WayResource, DepartmentResource

@admin.register(Way)
class WayAdmin(ImportExportModelAdmin):
    resource_class = WayResource
    formats = [base_formats.CSV, base_formats.XLSX, base_formats.JSON]
    list_display = ['way_id', 'name', 'destination']
    search_fields = ['name', 'destination']

@admin.register(Department)
class DepartmentAdmin(ImportExportModelAdmin):
    resource_class = DepartmentResource
    formats = [base_formats.CSV, base_formats.XLSX, base_formats.JSON]
    list_display = ['name', 'created_at']
    search_fields = ['name']
