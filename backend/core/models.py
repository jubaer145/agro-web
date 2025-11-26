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


class Event(models.Model):
    """Disease outbreak or veterinary event at a farm"""
    EVENT_TYPES = [
        ('vet_visit', 'Veterinary Visit'),
        ('vaccination', 'Vaccination'),
        ('disease_report', 'Disease Report'),
        ('mortality', 'Mortality'),
    ]
    
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]
    
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='events')
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    disease_suspected = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField()
    animals_affected = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_event_type_display()} at {self.farm.farmer_name}'s farm - {self.status}"


class CropIssue(models.Model):
    """Crop problem/outbreak reported by farmers"""
    PROBLEM_TYPE_CHOICES = [
        ('pest', 'Pest'),
        ('disease', 'Disease'),
        ('nutrient_deficiency', 'Nutrient Deficiency'),
        ('water_stress', 'Water Stress'),
        ('weed', 'Weed'),
        ('other', 'Other'),
    ]
    
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]
    
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='crop_issues')
    crop_type = models.CharField(max_length=100)  # e.g. wheat, barley, potatoes
    problem_type = models.CharField(max_length=50, choices=PROBLEM_TYPE_CHOICES)
    title = models.CharField(max_length=200)  # short farmer-facing title
    description = models.TextField()  # longer text describing problem
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    area_affected_ha = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    reported_via = models.CharField(max_length=20, default='mobile')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} at {self.farm.farmer_name}'s farm - {self.status}"
