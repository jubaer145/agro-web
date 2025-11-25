from rest_framework.test import APITestCase

class HealthAPITest(APITestCase):
    def test_health_endpoint(self):
        """Test that /api/health/ returns status 200 with {"status": "ok"}"""
        response = self.client.get('/api/health/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})
