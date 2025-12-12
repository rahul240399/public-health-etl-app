import requests

class WhoApiClient:
    """
    Service Layer: Handles external communication with the WHO GHO OData API.
    """
    
    BASE_URL = "https://ghoapi.azureedge.net/api"

    def get_countries(self):
        """
        Fetches the list of valid countries and their regions.
        Target Endpoint: /DIMENSION/COUNTRY/DimensionValues
        """
        url = f"{self.BASE_URL}/DIMENSION/COUNTRY/DimensionValues"
        return self._fetch_json(url)

    def get_health_data(self, indicator_code):
        """
        Fetches raw statistics for a specific health indicator.
        Target Endpoint: /{indicator_code}
        """
        url = f"{self.BASE_URL}/{indicator_code}"
        return self._fetch_json(url)

    def _fetch_json(self, url):
        """
        Helper method to execute GET requests with strict error handling.
        Returns empty list on failure or malformed data to ensure system stability.
        """
        try:
            # Timeout is critical to prevent the app from hanging indefinitely
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                # Validation: OData results must be wrapped in a 'value' key
                # This handles the "Malformed JSON" edge case from your test
                return data.get('value', [])
            
            # Log non-200 responses (simulated logging)
            print(f"[API ERROR] {url} returned status {response.status_code}")
            return []
            
        except requests.exceptions.RequestException as e:
            # Handles Timeouts, DNS errors, etc.
            print(f"[NETWORK ERROR] Failed to connect to {url}: {e}")
            return []