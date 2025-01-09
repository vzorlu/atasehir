from django.contrib import admin
from .models import Customer, Package, Devices, Department

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'company_name', 'tax_number', 'created_at', 'updated_at')
    search_fields = ('name', 'phone_number', 'company_name', 'tax_number')
    list_filter = ('created_at', 'updated_at', 'package')
    filter_horizontal = ('departments',)  # Çoklu seçim için

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_days', 'max_model', 'max_camera', 'max_device')
    search_fields = ('name',)
    list_filter = ('duration_days',)

@admin.register(Devices)
class DevicesAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    filter_horizontal = ('users',)  # Çoklu seçim için
