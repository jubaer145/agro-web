import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import District, Farm, Herd, Event


class Command(BaseCommand):
    help = 'Seeds the database with fake farm and herd data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding fake data...')
        
        # Clear existing data
        Event.objects.all().delete()
        Herd.objects.all().delete()
        Farm.objects.all().delete()
        District.objects.all().delete()
        
        # Create Districts
        districts_data = [
            {'name': 'Almaty Region', 'code': 'ALM'},
            {'name': 'Nur-Sultan Region', 'code': 'NUR'},
            {'name': 'Shymkent Region', 'code': 'SHY'},
        ]
        
        districts = []
        for data in districts_data:
            district = District.objects.create(**data)
            districts.append(district)
            self.stdout.write(self.style.SUCCESS(f'Created district: {district.name}'))
        
        # Kazakh/Central Asian names for farmers
        farmer_names = [
            'Almas Nurzhanov',
            'Aigul Bekova',
            'Yerlan Suleimenov',
            'Dinara Aitbekova',
            'Baurzhan Ospanov',
            'Aizhan Tokayeva',
            'Murat Kambarov',
            'Saule Abdullayeva',
            'Damir Zhumabayev',
            'Karlygash Ismailova',
        ]
        
        # Village names
        villages = [
            'Kaskelen', 'Talgar', 'Esik', 'Turgen', 'Issyk',
            'Aksu', 'Saryagash', 'Kentau', 'Arys', 'Shayan'
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
            
            # Generate realistic Kazakhstan phone numbers
            phone = f"+7 {random.randint(700, 799)} {random.randint(100, 999)} {random.randint(1000, 9999)}"
            
            # Generate location coordinates (Kazakhstan approximate bounds)
            # Latitude: 40.5° to 55.4° N
            # Longitude: 46.5° to 87.3° E
            location_lat = round(random.uniform(40.5, 55.4), 6)
            location_lng = round(random.uniform(46.5, 87.3), 6)
            
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
        event_types = ['disease_outbreak', 'vaccination', 'inspection', 'quarantine']
        statuses = ['reported', 'investigating', 'contained', 'resolved']
        
        disease_descriptions = [
            'Foot-and-mouth disease suspected in cattle herd',
            'Avian influenza detected in poultry',
            'Brucellosis outbreak in sheep',
            'Anthrax cases reported in cattle',
            'Newcastle disease in chickens'
        ]
        
        vaccination_descriptions = [
            'Routine vaccination campaign for cattle',
            'Seasonal flu vaccination for poultry',
            'Rabies vaccination for livestock',
            'Brucellosis vaccination program'
        ]
        
        inspection_descriptions = [
            'Routine veterinary inspection',
            'Annual health check for livestock',
            'Disease surveillance inspection',
            'Pre-sale health certificate inspection'
        ]
        
        quarantine_descriptions = [
            'Quarantine imposed due to disease outbreak',
            'Preventive quarantine for new animals',
            'Post-outbreak quarantine measures',
            'Movement restriction in affected area'
        ]
        
        description_map = {
            'disease_outbreak': disease_descriptions,
            'vaccination': vaccination_descriptions,
            'inspection': inspection_descriptions,
            'quarantine': quarantine_descriptions
        }
        
        num_events = random.randint(10, 15)
        events = []
        
        for i in range(num_events):
            farm = random.choice(farms)
            event_type = random.choice(event_types)
            status_choice = random.choice(statuses)
            description = random.choice(description_map[event_type])
            
            # Create event with varying timestamps (within last 30 days)
            event = Event.objects.create(
                farm=farm,
                event_type=event_type,
                status=status_choice,
                description=description
            )
            
            # Randomly adjust reported_at to be within last 30 days
            days_ago = random.randint(0, 30)
            event.reported_at = timezone.now() - timedelta(days=days_ago)
            event.save()
            
            events.append(event)
            self.stdout.write(
                f'Created event: {event.get_event_type_display()} at {farm.farmer_name}\'s farm - {status_choice}'
            )
        
        # Summary
        total_districts = District.objects.count()
        total_farms = Farm.objects.count()
        total_herds = Herd.objects.count()
        total_animals = sum(h.headcount for h in Herd.objects.all())
        total_events = Event.objects.count()
        
        self.stdout.write(self.style.SUCCESS('\n=== Summary ==='))
        self.stdout.write(self.style.SUCCESS(f'Districts created: {total_districts}'))
        self.stdout.write(self.style.SUCCESS(f'Farms created: {total_farms}'))
        self.stdout.write(self.style.SUCCESS(f'Herds created: {total_herds}'))
        self.stdout.write(self.style.SUCCESS(f'Total animals: {total_animals}'))
        self.stdout.write(self.style.SUCCESS(f'Events created: {total_events}'))
        self.stdout.write(self.style.SUCCESS('\nFake data seeded successfully!'))
