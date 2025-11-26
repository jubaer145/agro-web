from rest_framework.test import APITestCase
from django.urls import reverse
from .models import District, Farm, Herd, Event, CropIssue, CropIssue


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
            event_type='disease_report',
            status='new',
            description='Foot-and-mouth disease suspected in cattle herd',
            disease_suspected='Foot-and-mouth disease',
            animals_affected=10
        )
        
        self.event2 = Event.objects.create(
            farm=self.farm1,
            event_type='vaccination',
            status='resolved',
            description='Routine vaccination campaign for cattle'
        )
        
        self.event3 = Event.objects.create(
            farm=self.farm2,
            event_type='vet_visit',
            status='in_progress',
            description='Routine veterinary inspection'
        )
        
        self.event4 = Event.objects.create(
            farm=self.farm3,
            event_type='mortality',
            status='in_progress',
            description='Animal deaths reported',
            disease_suspected='Avian influenza',
            animals_affected=5
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
        self.assertEqual(event1_data['event_type'], 'disease_report')
        self.assertEqual(event1_data['status'], 'new')
        
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
        response = self.client.get(url, {'event_type': 'disease_report'})
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Should have 1 disease_report event
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['event_type'], 'disease_report')
    
    def test_events_filter_by_status(self):
        """Test filtering events by status"""
        url = reverse('event-list')
        response = self.client.get(url, {'status': 'new'})
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Should have 1 new event
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['status'], 'new')
    
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
        
        self.assertEqual(data['event_type'], 'disease_report')
        self.assertEqual(data['status'], 'new')
        self.assertIn('farm_summary', data)
    
    def test_event_patch_status_only(self):
        """Test PATCH endpoint allows updating only status field"""
        url = reverse('event-detail', args=[self.event1.id])
        response = self.client.patch(url, {'status': 'in_progress'}, format='json')
        
        self.assertEqual(response.status_code, 200)
        
        # Verify status was updated
        self.event1.refresh_from_db()
        self.assertEqual(self.event1.status, 'in_progress')
    
    def test_event_patch_status_invalid_field(self):
        """Test PATCH endpoint rejects updates to fields other than status"""
        url = reverse('event-detail', args=[self.event1.id])
        response = self.client.patch(
            url,
            {'status': 'in_progress', 'description': 'New description'},
            format='json'
        )
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())
        
        # Verify nothing was updated
        self.event1.refresh_from_db()
        self.assertEqual(self.event1.status, 'new')
        self.assertEqual(self.event1.description, 'Foot-and-mouth disease suspected in cattle herd')


class DashboardAPITest(APITestCase):
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
            village='Kaskelen'
        )
        
        self.farm2 = Farm.objects.create(
            district=self.district2,
            farmer_name='Yerlan Suleimenov',
            phone='+7 703 456 7890',
            village='Aksu'
        )
        
        # Create herds
        Herd.objects.create(farm=self.farm1, animal_type='cattle', headcount=25)
        Herd.objects.create(farm=self.farm2, animal_type='sheep', headcount=100)
        
        # Create events
        Event.objects.create(
            farm=self.farm1,
            event_type='disease_report',
            status='new',
            description='Test outbreak',
            disease_suspected='Foot-and-mouth disease',
            animals_affected=10
        )
        
        Event.objects.create(
            farm=self.farm2,
            event_type='vaccination',
            status='resolved',
            description='Routine vaccination'
        )
    
    def test_dashboard_summary_all(self):
        """Test dashboard summary without filter"""
        url = reverse('dashboard-summary')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertEqual(data['total_farms'], 2)
        self.assertEqual(data['total_animals'], 125)
        self.assertEqual(data['open_outbreaks'], 1)
        self.assertEqual(len(data['farms_by_district']), 2)
    
    def test_dashboard_summary_filtered(self):
        """Test dashboard summary with district filter"""
        url = reverse('dashboard-summary')
        response = self.client.get(url, {'district': 'ALM'})
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertEqual(data['total_farms'], 1)
        self.assertEqual(data['total_animals'], 25)
        self.assertEqual(data['open_outbreaks'], 1)


class CropIssueAPITest(APITestCase):
    def setUp(self):
        """Set up test data for crop issues"""
        # Create districts
        self.district1 = District.objects.create(name='Almaty Region', code='ALM')
        self.district2 = District.objects.create(name='Nur-Sultan Region', code='NUR')
        
        # Create farms
        self.farm1 = Farm.objects.create(
            district=self.district1,
            farmer_name='Almas Nurzhanov',
            phone='+7 701 234 5678',
            village='Kaskelen'
        )
        
        self.farm2 = Farm.objects.create(
            district=self.district1,
            farmer_name='Aigul Bekova',
            phone='+7 702 345 6789',
            village='Talgar'
        )
        
        self.farm3 = Farm.objects.create(
            district=self.district2,
            farmer_name='Yerlan Suleimenov',
            phone='+7 703 456 7890',
            village='Aksu'
        )
        
        # Create crop issues
        self.crop_issue1 = CropIssue.objects.create(
            farm=self.farm1,
            crop_type='wheat',
            problem_type='disease',
            title='Rust disease on wheat',
            description='Severe rust disease affecting wheat crops',
            severity='high',
            area_affected_ha=5.5,
            status='new',
            reported_via='mobile'
        )
        
        self.crop_issue2 = CropIssue.objects.create(
            farm=self.farm1,
            crop_type='barley',
            problem_type='pest',
            title='Aphid infestation',
            description='Aphids spreading across barley field',
            severity='medium',
            area_affected_ha=2.0,
            status='in_progress',
            reported_via='mobile'
        )
        
        self.crop_issue3 = CropIssue.objects.create(
            farm=self.farm2,
            crop_type='potatoes',
            problem_type='water_stress',
            title='Drought stress visible',
            description='Lack of irrigation causing crop stress',
            severity='medium',
            area_affected_ha=3.5,
            status='new',
            reported_via='web'
        )
        
        self.crop_issue4 = CropIssue.objects.create(
            farm=self.farm3,
            crop_type='corn',
            problem_type='nutrient_deficiency',
            title='Yellowing leaves',
            description='Nitrogen deficiency suspected in corn field',
            severity='low',
            area_affected_ha=1.5,
            status='resolved',
            reported_via='phone'
        )
    
    def test_list_crop_issues_returns_data_with_farm_summary(self):
        """Test that /api/crop-issues/ returns list with farm_summary"""
        url = reverse('cropissue-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Should have 4 crop issues
        self.assertEqual(len(data), 4)
        
        # Check first crop issue has farm_summary
        issue1_data = next(c for c in data if c['id'] == self.crop_issue1.id)
        self.assertEqual(issue1_data['crop_type'], 'wheat')
        self.assertEqual(issue1_data['problem_type'], 'disease')
        self.assertEqual(issue1_data['severity'], 'high')
        self.assertEqual(issue1_data['status'], 'new')
        
        # Check farm_summary is embedded with expected keys
        self.assertIn('farm_summary', issue1_data)
        farm_summary = issue1_data['farm_summary']
        self.assertEqual(farm_summary['farm_id'], self.farm1.id)
        self.assertEqual(farm_summary['farmer_name'], 'Almas Nurzhanov')
        self.assertEqual(farm_summary['village'], 'Kaskelen')
        self.assertEqual(farm_summary['district_name'], 'Almaty Region')
    
    def test_filter_crop_issues_by_district_and_status(self):
        """Test filtering crop issues by district and status"""
        url = reverse('cropissue-list')
        
        # Filter by district
        response = self.client.get(url, {'district': 'ALM'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 3)  # 3 issues in Almaty region
        for issue in data:
            self.assertEqual(issue['farm_summary']['district_name'], 'Almaty Region')
        
        # Filter by status
        response = self.client.get(url, {'status': 'new'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)  # 2 new issues
        for issue in data:
            self.assertEqual(issue['status'], 'new')
        
        # Filter by both district and status
        response = self.client.get(url, {'district': 'ALM', 'status': 'new'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)  # 2 new issues in Almaty
        for issue in data:
            self.assertEqual(issue['status'], 'new')
            self.assertEqual(issue['farm_summary']['district_name'], 'Almaty Region')
        
        # Filter by crop_type
        response = self.client.get(url, {'crop_type': 'wheat'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['crop_type'], 'wheat')
        
        # Filter by problem_type
        response = self.client.get(url, {'problem_type': 'disease'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['problem_type'], 'disease')
        
        # Filter by severity
        response = self.client.get(url, {'severity': 'high'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['severity'], 'high')
    
    def test_patch_crop_issue_status_only(self):
        """Test PATCH endpoint allows updating only status field"""
        url = reverse('cropissue-detail', args=[self.crop_issue1.id])
        
        # Test successful status update
        response = self.client.patch(url, {'status': 'in_progress'}, format='json')
        self.assertEqual(response.status_code, 200)
        
        # Verify status was updated
        self.crop_issue1.refresh_from_db()
        self.assertEqual(self.crop_issue1.status, 'in_progress')
        
        # Test rejection when trying to update other fields
        original_title = self.crop_issue1.title
        response = self.client.patch(
            url,
            {'status': 'resolved', 'title': 'New title'},
            format='json'
        )
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())
        self.assertIn('Only', response.json()['error'])
        
        # Verify nothing was updated
        self.crop_issue1.refresh_from_db()
        self.assertEqual(self.crop_issue1.status, 'in_progress')  # Still in_progress from before
        self.assertEqual(self.crop_issue1.title, original_title)  # Title unchanged
