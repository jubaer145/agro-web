from django.db import models


class District(models.Model):
    """Administrative district/region"""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.code})"


class Farm(models.Model):
    """Farm registration with location and owner details"""
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='farms')
    farmer_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    village = models.CharField(max_length=100)
    location_lat = models.FloatField(null=True, blank=True)
    location_lng = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.farmer_name} - {self.village}"


class Herd(models.Model):
    """Animal herd associated with a farm"""
    ANIMAL_TYPES = [
        ('cattle', 'Cattle'),
        ('sheep', 'Sheep'),
        ('goat', 'Goat'),
        ('horse', 'Horse'),
        ('poultry', 'Poultry'),
    ]
    
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='herds')
    animal_type = models.CharField(max_length=50, choices=ANIMAL_TYPES)
    headcount = models.IntegerField()
    
    class Meta:
        ordering = ['animal_type']
    
    def __str__(self):
        return f"{self.headcount} {self.animal_type} at {self.farm.farmer_name}'s farm"
