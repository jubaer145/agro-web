from rest_framework.test import APITestCase
from django.urls import reverse
from .models import District, Farm, Herd, Event


class HealthAPITest(APITestCase):
    def test_health_endpoint(self):
        """Test that /api/health/ returns status 200 with {"status": "ok"}"""
        response = self.client.get('/api/health/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})


class FarmAPITest(APITestCase):
    def setUp(self):
        """Set up test data"""
        # Create districts
        self.district1 = District.objects.create(name='Almaty Region', code='ALM')
        self.district2 = District.objects.create(name='Nur-Sultan Region', code='NUR')
        
        # Create farms
        self.farm1 = Farm.objects.create(
            district=self.district1,
            farmer_name='Almas Nurzhanov',
            phone='+7 701 234 5678',
            village='Kaskelen',
            location_lat=43.2,
            location_lng=76.6
        )
        
        self.farm2 = Farm.objects.create(
            district=self.district1,
            farmer_name='Aigul Bekova',
            phone='+7 702 345 6789',
            village='Talgar',
            location_lat=43.3,
            location_lng=77.2
        )
        
        self.farm3 = Farm.objects.create(
            district=self.district2,
            farmer_name='Yerlan Suleimenov',
            phone='+7 703 456 7890',
            village='Aksu',
            location_lat=51.1,
            location_lng=71.4
        )
        
        # Create herds
        Herd.objects.create(farm=self.farm1, animal_type='cattle', headcount=25)
        Herd.objects.create(farm=self.farm1, animal_type='sheep', headcount=100)
        
        Herd.objects.create(farm=self.farm2, animal_type='goat', headcount=50)
        
        Herd.objects.create(farm=self.farm3, animal_type='cattle', headcount=30)
        Herd.objects.create(farm=self.farm3, animal_type='horse', headcount=10)
    
    def test_farms_list(self):
        """Test that /api/farms/ returns list of farms with nested herds"""
        url = reverse('farm-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Should have 3 farms
        self.assertEqual(len(data), 3)
        
        # Check first farm has nested data
        farm1_data = next(f for f in data if f['farmer_name'] == 'Almas Nurzhanov')
        self.assertEqual(farm1_data['district_name'], 'Almaty Region')
        self.assertEqual(farm1_data['district_code'], 'ALM')
        self.assertEqual(farm1_data['village'], 'Kaskelen')
        self.assertEqual(len(farm1_data['herds']), 2)
        self.assertEqual(farm1_data['total_animals'], 125)
    
    def test_farms_filter_by_district(self):
        """Test filtering farms by district code"""
        url = reverse('farm-list')
        response = self.client.get(url, {'district': 'ALM'})
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Should only have farms from Almaty region
        self.assertEqual(len(data), 2)
        for farm in data:
            self.assertEqual(farm['district_code'], 'ALM')
    
    def test_farms_search_by_farmer_name(self):
        """Test searching farms by farmer name"""
        url = reverse('farm-list')
        response = self.client.get(url, {'search': 'Almas'})
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Should find 1 farm
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['farmer_name'], 'Almas Nurzhanov')
    
    def test_farms_search_by_phone(self):
        """Test searching farms by phone number"""
        url = reverse('farm-list')
        response = self.client.get(url, {'search': '702'})
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Should find 1 farm
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['farmer_name'], 'Aigul Bekova')
    
    def test_farms_search_case_insensitive(self):
        """Test that search is case-insensitive"""
        url = reverse('farm-list')
        response = self.client.get(url, {'search': 'aigul'})
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Should find 1 farm
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['farmer_name'], 'Aigul Bekova')
    
    def test_farm_detail(self):
        """Test retrieving a single farm"""
        url = reverse('farm-detail', args=[self.farm1.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertEqual(data['farmer_name'], 'Almas Nurzhanov')
        self.assertEqual(data['village'], 'Kaskelen')
        self.assertEqual(len(data['herds']), 2)


class DistrictAPITest(APITestCase):
    def setUp(self):
        """Set up test data"""
        District.objects.create(name='Almaty Region', code='ALM')
        District.objects.create(name='Nur-Sultan Region', code='NUR')
    
    def test_districts_list(self):
        """Test that /api/districts/ returns list of districts"""
        url = reverse('district-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertEqual(len(data), 2)
        self.assertTrue(any(d['code'] == 'ALM' for d in data))
        self.assertTrue(any(d['code'] == 'NUR' for d in data))


class EventAPITest(APITestCase):
    def setUp(self):
        """Set up test data for events"""
        # Create districts
        self.district1 = District.objects.create(name='Almaty Region', code='ALM')
        self.district2 = District.objects.create(name='Nur-Sultan Region', code='NUR')
        
        # Create farms
        self.farm1 = Farm.objects.create(
            district=self.district1,
            farmer_name='Almas Nurzhanov',
            phone='+7 701 234 5678',
            village='Kaskelen',
            location_lat=43.2,
            location_lng=76.6
        )
        
        self.farm2 = Farm.objects.create(
            district=self.district1,
            farmer_name='Aigul Bekova',
            phone='+7 702 345 6789',
            village='Talgar',
            location_lat=43.3,
            location_lng=77.2
        )
        
        self.farm3 = Farm.objects.create(
            district=self.district2,
            farmer_name='Yerlan Suleimenov',
            phone='+7 703 456 7890',
            village='Aksu',
            location_lat=51.1,
            location_lng=71.4
        )
        
        # Create events
        self.event1 = Event.objects.create(
            farm=self.farm1,
            event_type='disease_outbreak',
            status='reported',
            description='Foot-and-mouth disease suspected in cattle herd'
        )
        
        self.event2 = Event.objects.create(
            farm=self.farm1,
            event_type='vaccination',
            status='resolved',
            description='Routine vaccination campaign for cattle'
        )
        
        self.event3 = Event.objects.create(
            farm=self.farm2,
            event_type='inspection',
            status='investigating',
            description='Routine veterinary inspection'
        )
        
        self.event4 = Event.objects.create(
            farm=self.farm3,
            event_type='quarantine',
            status='contained',
            description='Quarantine imposed due to disease outbreak'
        )
    
    def test_events_list(self):
        """Test that /api/events/ returns list of events with nested farm_summary"""
        url = reverse('event-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Should have 4 events
        self.assertEqual(len(data), 4)
        
        # Check first event has nested farm_summary
        event1_data = next(e for e in data if e['id'] == self.event1.id)
        self.assertEqual(event1_data['event_type'], 'disease_outbreak')
        self.assertEqual(event1_data['status'], 'reported')
        
        # Check farm_summary is embedded
        self.assertIn('farm_summary', event1_data)
        farm_summary = event1_data['farm_summary']
        self.assertEqual(farm_summary['farmer_name'], 'Almas Nurzhanov')
        self.assertEqual(farm_summary['village'], 'Kaskelen')
        self.assertEqual(farm_summary['district_name'], 'Almaty Region')
    
    def test_events_filter_by_district(self):
        """Test filtering events by district code"""
        url = reverse('event-list')
        response = self.client.get(url, {'district': 'ALM'})
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Should have 3 events from Almaty region
        self.assertEqual(len(data), 3)
        for event in data:
            self.assertEqual(event['farm_summary']['district_name'], 'Almaty Region')
    
    def test_events_filter_by_event_type(self):
        """Test filtering events by event_type"""
        url = reverse('event-list')
        response = self.client.get(url, {'event_type': 'disease_outbreak'})
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Should have 1 disease_outbreak event
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['event_type'], 'disease_outbreak')
    
    def test_events_filter_by_status(self):
        """Test filtering events by status"""
        url = reverse('event-list')
        response = self.client.get(url, {'status': 'reported'})
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Should have 1 reported event
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['status'], 'reported')
    
    def test_events_filter_multiple(self):
        """Test filtering events by multiple parameters"""
        url = reverse('event-list')
        response = self.client.get(url, {'district': 'ALM', 'status': 'resolved'})
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Should have 1 resolved event in Almaty region
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['status'], 'resolved')
        self.assertEqual(data[0]['farm_summary']['district_name'], 'Almaty Region')
    
    def test_event_detail(self):
        """Test retrieving a single event"""
        url = reverse('event-detail', args=[self.event1.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertEqual(data['event_type'], 'disease_outbreak')
        self.assertEqual(data['status'], 'reported')
        self.assertIn('farm_summary', data)
    
    def test_event_patch_status_only(self):
        """Test PATCH endpoint allows updating only status field"""
        url = reverse('event-detail', args=[self.event1.id])
        response = self.client.patch(url, {'status': 'investigating'}, format='json')
        
        self.assertEqual(response.status_code, 200)
        
        # Verify status was updated
        self.event1.refresh_from_db()
        self.assertEqual(self.event1.status, 'investigating')
    
    def test_event_patch_status_invalid_field(self):
        """Test PATCH endpoint rejects updates to fields other than status"""
        url = reverse('event-detail', args=[self.event1.id])
        response = self.client.patch(
            url,
            {'status': 'investigating', 'description': 'New description'},
            format='json'
        )
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())
        
        # Verify nothing was updated
        self.event1.refresh_from_db()
        self.assertEqual(self.event1.status, 'reported')
        self.assertEqual(self.event1.description, 'Foot-and-mouth disease suspected in cattle herd')
