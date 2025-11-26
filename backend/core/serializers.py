from rest_framework import serializers
from .models import District, Farm, Herd, Event


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


class EventSerializer(serializers.ModelSerializer):
    """Serializer for Event model with embedded farm summary"""
    event_type_display = serializers.CharField(source='get_event_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    farm_summary = serializers.SerializerMethodField()
    
    class Meta:
        model = Event
        fields = [
            'id',
            'farm',
            'farm_summary',
            'event_type',
            'event_type_display',
            'disease_suspected',
            'description',
            'animals_affected',
            'status',
            'status_display',
            'created_at'
        ]
        read_only_fields = ['created_at']
    
    def get_farm_summary(self, obj):
        """Embed farm details: farm_id, farmer_name, village, district_name"""
        return {
            'farm_id': obj.farm.id,
            'farmer_name': obj.farm.farmer_name,
            'village': obj.farm.village,
            'district_name': obj.farm.district.name
        }
