import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app

class TestWebRoutes(unittest.TestCase):
    
    def setUp(self):
        """
        Sets up a 'Test Client' that simulates a web browser.
        This allows us to test URLs without running the actual server.
        """
        print("\n--- Starting Web Route Test ---")
        self.app = create_app(test_config=True) # We will create this factory function next
        self.client = self.app.test_client()

    def tearDown(self):
        print("--- Web Test Finished ---\n")

    def test_home_page_loads(self):
        """Verifies the index page returns HTTP 200 OK."""
        print("[ACTION] Requesting GET / ...")
        response = self.client.get('/')
        
        print(f"[ASSERT] Status Code should be 200... (Got: {response.status_code})")
        self.assertEqual(response.status_code, 200)

    @patch('routes.main_routes.WhoApiClient')
    @patch('routes.main_routes.SqliteHealthRepository')
    def test_load_data_route(self, MockRepo, MockApiClient):
        """
        Verifies that hitting /load_data triggers the ETL pipeline.
        Mocks the heavy lifting (API & DB) to focus on the Controller logic.
        """
        print("[ACTION] Requesting POST /load_data ...")
        
        # Setup Mocks
        mock_api = MockApiClient.return_value
        mock_api.get_countries.return_value = [{"Code": "GBR", "Title": "UK", "ParentDimension": "EURO"}]
        mock_api.get_health_data.return_value = []
        
        # Execute Request
        response = self.client.post('/load_data', follow_redirects=True)
        
        print(f"[ASSERT] Should redirect and load dashboard (HTTP 200)... (Got: {response.status_code})")
        self.assertEqual(response.status_code, 200)
        
        # Verify the Controller called the right Model methods
        print("[ASSERT] Checking if API client was called...")
        mock_api.get_countries.assert_called_once()
        mock_api.get_health_data.assert_called()

    @patch('routes.main_routes.SqliteHealthRepository')
    def test_dashboard_route(self, MockRepo):
        """Verifies the dashboard queries the repository."""
        print("[ACTION] Requesting GET /dashboard ...")
        
        # Mock DB returning some data
        mock_repo = MockRepo.return_value
        mock_repo.fetch_facts_by_year.return_value = [
            {'country': 'France', 'value': 82.5, 'sex': 'Male'}
        ]
        
        response = self.client.get('/dashboard')
        
        print(f"[ASSERT] Status Code should be 200... (Got: {response.status_code})")
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()