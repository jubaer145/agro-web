from django.contrib import admin
from .models import District, Farm, Herd


class HerdInline(admin.TabularInline):
    model = Herd
    extra = 1


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    search_fields = ['name', 'code']


@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ['farmer_name', 'village', 'district', 'phone', 'created_at']
    list_filter = ['district', 'created_at']
    search_fields = ['farmer_name', 'phone', 'village']
    inlines = [HerdInline]


@admin.register(Herd)
class HerdAdmin(admin.ModelAdmin):
    list_display = ['farm', 'animal_type', 'headcount']
    list_filter = ['animal_type']
    search_fields = ['farm__farmer_name']
