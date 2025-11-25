from rest_framework import serializers
from .models import District, Farm, Herd


class DistrictSerializer(serializers.ModelSerializer):
    """Serializer for District model"""
    class Meta:
        model = District
        fields = ['id', 'name', 'code']


class HerdSerializer(serializers.ModelSerializer):
    """Serializer for Herd model"""
    animal_type_display = serializers.CharField(source='get_animal_type_display', read_only=True)
    
    class Meta:
        model = Herd
        fields = ['id', 'animal_type', 'animal_type_display', 'headcount']


class FarmSerializer(serializers.ModelSerializer):
    """Serializer for Farm model with nested district and herds"""
    district_name = serializers.CharField(source='district.name', read_only=True)
    district_code = serializers.CharField(source='district.code', read_only=True)
    herds = HerdSerializer(many=True, read_only=True)
    total_animals = serializers.SerializerMethodField()
    
    class Meta:
        model = Farm
        fields = [
            'id', 
            'farmer_name', 
            'phone', 
            'village', 
            'location_lat', 
            'location_lng',
            'district', 
            'district_name', 
            'district_code',
            'herds',
            'total_animals',
            'created_at',
            'updated_at'
        ]
    
    def get_total_animals(self, obj):
        """Calculate total number of animals across all herds"""
        return sum(herd.headcount for herd in obj.herds.all())
