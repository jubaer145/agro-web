import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import District, Farm, Herd, Event, CropIssue


class Command(BaseCommand):
    help = 'Seeds the database with fake farm and herd data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding fake data...')
        
        # Clear existing data
        CropIssue.objects.all().delete()
        Event.objects.all().delete()
        Herd.objects.all().delete()
        Farm.objects.all().delete()
        District.objects.all().delete()
        
        # Create Districts
        districts_data = [
            {'name': 'Chuy Region', 'code': 'CHU'},
            {'name': 'Issyk-Kul Region', 'code': 'IKL'},
            {'name': 'Osh Region', 'code': 'OSH'},
        ]
        
        districts = []
        for data in districts_data:
            district = District.objects.create(**data)
            districts.append(district)
            self.stdout.write(self.style.SUCCESS(f'Created district: {district.name}'))
        
        # Kyrgyz names for farmers
        farmer_names = [
            'Bolot Mamatov',
            'Aigul Bekova',
            'Nurlan Toktomushev',
            'Dinara Aitbekova',
            'Azamat Kadyrov',
            'Aizhan Tokayeva',
            'Murat Asanov',
            'Cholpon Abdullayeva',
            'Bektur Karimov',
            'Ainura Isaeva',
        ]
        
        # Village names (Kyrgyzstan)
        villages = [
            'Tokmok', 'Kant', 'Kemin', 'Cholpon-Ata', 'Karakol',
            'Kara-Suu', 'Jalal-Abad', 'Naryn', 'Talas', 'Balykchy'
        ]
        
        # Animal types and typical herd sizes
        animal_data = [
            ('cattle', (5, 50)),
            ('sheep', (20, 200)),
            ('goat', (10, 100)),
            ('horse', (2, 20)),
            ('poultry', (50, 500)),
        ]
        
        # Create Farms (6-10 farms)
        num_farms = random.randint(6, 10)
        farms = []
        
        for i in range(num_farms):
            district = random.choice(districts)
            farmer_name = random.choice(farmer_names)
            village = random.choice(villages)
            
            # Generate realistic Kyrgyzstan phone numbers
            phone = f"+996 {random.randint(500, 799)} {random.randint(100, 999)} {random.randint(100, 999)}"
            
            # Generate location coordinates (Kyrgyzstan approximate bounds)
            # Latitude: 39.2° to 43.2° N
            # Longitude: 69.3° to 80.3° E
            location_lat = round(random.uniform(39.2, 43.2), 6)
            location_lng = round(random.uniform(69.3, 80.3), 6)
            
            farm = Farm.objects.create(
                district=district,
                farmer_name=farmer_name,
                phone=phone,
                village=village,
                location_lat=location_lat,
                location_lng=location_lng
            )
            farms.append(farm)
            self.stdout.write(f'Created farm: {farmer_name} in {village}, {district.name}')
            
            # Create 1-3 herds per farm
            num_herds = random.randint(1, 3)
            selected_animals = random.sample(animal_data, num_herds)
            
            for animal_type, (min_count, max_count) in selected_animals:
                headcount = random.randint(min_count, max_count)
                herd = Herd.objects.create(
                    farm=farm,
                    animal_type=animal_type,
                    headcount=headcount
                )
                self.stdout.write(f'  - Added herd: {headcount} {animal_type}')
        
        # Create Events (10-15 events)
        event_types = ['vet_visit', 'vaccination', 'disease_report', 'mortality']
        statuses = ['new', 'in_progress', 'resolved']
        
        diseases = [
            'Foot-and-mouth disease',
            'Avian influenza',
            'Brucellosis',
            'Anthrax',
            'Newcastle disease',
            'Tuberculosis',
            'Mastitis',
            'Blackleg'
        ]
        
        vet_visit_descriptions = [
            'Routine veterinary checkup',
            'Annual health examination',
            'Follow-up visit for treatment',
            'Pre-breeding health assessment'
        ]
        
        vaccination_descriptions = [
            'Routine vaccination campaign',
            'Seasonal flu vaccination',
            'Rabies vaccination program',
            'Brucellosis vaccination'
        ]
        
        disease_report_descriptions = [
            'Unusual symptoms observed in herd',
            'Suspected disease outbreak reported',
            'Animals showing signs of illness',
            'Disease symptoms detected during inspection'
        ]
        
        mortality_descriptions = [
            'Animal deaths reported',
            'Multiple casualties in herd',
            'Sudden death incident',
            'Disease-related mortality'
        ]
        
        description_map = {
            'vet_visit': vet_visit_descriptions,
            'vaccination': vaccination_descriptions,
            'disease_report': disease_report_descriptions,
            'mortality': mortality_descriptions
        }
        
        num_events = random.randint(10, 15)
        events = []
        
        for i in range(num_events):
            farm = random.choice(farms)
            event_type = random.choice(event_types)
            status_choice = random.choice(statuses)
            description = random.choice(description_map[event_type])
            
            # Set disease_suspected for disease_report and mortality events
            disease_suspected = None
            if event_type in ['disease_report', 'mortality']:
                disease_suspected = random.choice(diseases) if random.random() > 0.3 else None
            
            # Set animals_affected for disease_report and mortality events
            animals_affected = None
            if event_type in ['disease_report', 'mortality']:
                animals_affected = random.randint(1, 50)
            
            # Create event with varying timestamps (within last 30 days)
            event = Event.objects.create(
                farm=farm,
                event_type=event_type,
                status=status_choice,
                description=description,
                disease_suspected=disease_suspected,
                animals_affected=animals_affected
            )
            
            # Randomly adjust created_at to be within last 30 days
            days_ago = random.randint(0, 30)
            event.created_at = timezone.now() - timedelta(days=days_ago)
            event.save()
            
            events.append(event)
            
            event_info = f'Created event: {event.get_event_type_display()} at {farm.farmer_name}\'s farm - {status_choice}'
            if disease_suspected:
                event_info += f' ({disease_suspected})'
            self.stdout.write(event_info)
        
        # Create CropIssues (8-15 crop issues)
        crop_types = ['wheat', 'barley', 'potatoes', 'corn', 'tomatoes', 'carrots', 'onions', 'sunflower']
        problem_types = ['pest', 'disease', 'nutrient_deficiency', 'water_stress', 'weed', 'other']
        severities = ['low', 'medium', 'high']
        crop_statuses = ['new', 'in_progress', 'resolved']
        
        pest_titles = [
            'Aphid infestation in crops',
            'Locust swarm damage',
            'Cutworm damage observed',
            'Beetle infestation spreading'
        ]
        
        disease_titles = [
            'Fungal infection spreading',
            'Rust disease on wheat',
            'Blight affecting potatoes',
            'Wilt disease detected'
        ]
        
        nutrient_titles = [
            'Yellowing leaves - nitrogen deficiency',
            'Poor growth - phosphorus deficiency',
            'Leaf discoloration - potassium deficiency',
            'Stunted growth - micronutrient deficiency'
        ]
        
        water_titles = [
            'Drought stress visible',
            'Wilting from lack of water',
            'Irrigation system failure',
            'Waterlogging in field'
        ]
        
        weed_titles = [
            'Heavy weed infestation',
            'Invasive weeds spreading',
            'Weed competition reducing yield',
            'Thistle infestation'
        ]
        
        other_titles = [
            'Hail damage to crops',
            'Frost damage observed',
            'Wind damage to plants',
            'Unexpected crop failure'
        ]
        
        title_map = {
            'pest': pest_titles,
            'disease': disease_titles,
            'nutrient_deficiency': nutrient_titles,
            'water_stress': water_titles,
            'weed': weed_titles,
            'other': other_titles
        }
        
        num_crop_issues = random.randint(8, 15)
        crop_issues = []
        
        # Ensure at least 2-3 high severity disease/pest cases
        high_severity_count = 0
        medium_severity_count = 0
        
        for i in range(num_crop_issues):
            farm = random.choice(farms)
            crop_type = random.choice(crop_types)
            
            # Ensure we have at least 2-3 high severity disease/pest and 2-3 medium water_stress/nutrient_deficiency
            if i < 3 and high_severity_count < 3:
                problem_type = random.choice(['pest', 'disease'])
                severity = 'high'
                high_severity_count += 1
            elif i >= 3 and i < 6 and medium_severity_count < 3:
                problem_type = random.choice(['water_stress', 'nutrient_deficiency'])
                severity = 'medium'
                medium_severity_count += 1
            else:
                problem_type = random.choice(problem_types)
                severity = random.choice(severities)
            
            title = random.choice(title_map[problem_type])
            status_choice = random.choice(crop_statuses)
            area_affected = round(random.uniform(0.5, 10.0), 2)
            
            description_templates = [
                f'Farmers report {problem_type} affecting {crop_type} crops. Approximately {area_affected} hectares affected. Immediate attention required.',
                f'{crop_type} field showing signs of {problem_type}. Area: {area_affected} ha. Requesting assistance.',
                f'Significant {problem_type} issue detected in {crop_type} cultivation. Estimated impact: {area_affected} ha.',
                f'{crop_type} crops experiencing {problem_type}. Coverage area: {area_affected} hectares. Farmer concerned about yield loss.'
            ]
            
            description = random.choice(description_templates)
            
            crop_issue = CropIssue.objects.create(
                farm=farm,
                crop_type=crop_type,
                problem_type=problem_type,
                title=title,
                description=description,
                severity=severity,
                area_affected_ha=area_affected,
                status=status_choice,
                reported_via=random.choice(['mobile', 'web', 'phone'])
            )
            
            # Randomly adjust created_at to be within last 30 days
            days_ago = random.randint(0, 30)
            crop_issue.created_at = timezone.now() - timedelta(days=days_ago)
            crop_issue.save()
            
            crop_issues.append(crop_issue)
            
            self.stdout.write(f'Created crop issue: {title} ({severity}) - {crop_type} at {farm.farmer_name}\'s farm')
        
        # Summary
        total_districts = District.objects.count()
        total_farms = Farm.objects.count()
        total_herds = Herd.objects.count()
        total_animals = sum(h.headcount for h in Herd.objects.all())
        total_events = Event.objects.count()
        total_crop_issues = CropIssue.objects.count()
        
        self.stdout.write(self.style.SUCCESS('\n=== Summary ==='))
        self.stdout.write(self.style.SUCCESS(f'Districts created: {total_districts}'))
        self.stdout.write(self.style.SUCCESS(f'Farms created: {total_farms}'))
        self.stdout.write(self.style.SUCCESS(f'Herds created: {total_herds}'))
        self.stdout.write(self.style.SUCCESS(f'Total animals: {total_animals}'))
        self.stdout.write(self.style.SUCCESS(f'Events created: {total_events}'))
        self.stdout.write(self.style.SUCCESS(f'Crop issues created: {total_crop_issues}'))
        self.stdout.write(self.style.SUCCESS('\nFake data seeded successfully!'))
