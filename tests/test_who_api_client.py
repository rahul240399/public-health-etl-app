import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import requests

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.who_api_client import WhoApiClient

class TestWhoApiClient(unittest.TestCase):
    
    def setUp(self):
        print("\n--- Starting API Client Test ---")
        self.client = WhoApiClient()

    def tearDown(self):
        print("--- Test Finished ---\n")

    @patch('models.who_api_client.requests.get')
    def test_fetch_countries_success(self, mock_get):
        """Verifies that the client parses a standard 200 OK response correctly."""
        print("[ACTION] Mocking successful Country API response...")
        
        # Configure the Mock to return valid JSON
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "value": [
                {"Code": "GBR", "Title": "United Kingdom", "ParentDimension": "EURO"},
                {"Code": "FRA", "Title": "France", "ParentDimension": "EURO"}
            ]
        }
        mock_get.return_value = mock_response

        # Execute
        print("[ACTION] Calling get_countries()...")
        result = self.client.get_countries()

        # Verify
        print(f"[ASSERT] Checking if 2 countries were loaded... (Got: {len(result)})")
        self.assertEqual(len(result), 2)
        
        print(f"[ASSERT] Checking first country code... (Got: {result[0]['Code']})")
        self.assertEqual(result[0]['Code'], "GBR")

    @patch('models.who_api_client.requests.get')
    def test_fetch_returns_empty_on_404(self, mock_get):
        """Edge Case: Verifies that a 404 Not Found error returns an empty list."""
        print("[ACTION] Mocking 404 API Error...")
        
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        print("[ACTION] Calling get_countries() expecting failure handling...")
        result = self.client.get_countries()

        print(f"[ASSERT] Result should be empty list... (Got: {result})")
        self.assertEqual(result, [])

    @patch('models.who_api_client.requests.get')
    def test_network_timeout_handling(self, mock_get):
        """Edge Case: Verifies that a Connection Timeout is handled gracefully."""
        print("[ACTION] Simulating Network Timeout exception...")
        
        # Configure Mock to raise an exception instead of returning a value
        mock_get.side_effect = requests.exceptions.Timeout("Connection timed out")

        result = self.client.get_health_data("WHOSIS_000001")

        print(f"[ASSERT] System should survive timeout and return []... (Got: {result})")
        self.assertEqual(result, [])

    @patch('models.who_api_client.requests.get')
    def test_malformed_json_response(self, mock_get):
        """Edge Case: Verifies behavior when API returns valid 200 OK but unexpected JSON format."""
        print("[ACTION] Mocking malformed JSON (missing 'value' key)...")
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        # The API returns data, but not inside the expected "value" list wrapper
        mock_response.json.return_value = {"error": "Invalid query"} 
        mock_get.return_value = mock_response

        result = self.client.get_countries()

        print(f"[ASSERT] Should handle missing keys by returning empty list... (Got: {result})")
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()