import unittest
import sqlite3
import os
import sys

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Specific Imports reflecting Domain Models
from models.sqlite_repository import SqliteHealthRepository
from models.who_code_normalizer import WhoCodeNormalizer

class TestWhoHealthService(unittest.TestCase):
    
    def setUp(self):
        """
        Initializes a fresh SQLite database for isolation before each test.
        """
        self.test_db_path = "test_who_health.db"
        self.repo = SqliteHealthRepository(self.test_db_path)

    def tearDown(self):
        """
        Closes connection and deletes the test database file.
        """
        self.repo.close_connection()
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

    def test_normalize_sex_codes(self):
        """
        Verifies 'MLE' converts to 'Male' and unknown codes return as-is.
        """
        self.assertEqual(WhoCodeNormalizer.normalize_sex("MLE"), "Male")
        self.assertEqual(WhoCodeNormalizer.normalize_sex("FMLE"), "Female")
        self.assertEqual(WhoCodeNormalizer.normalize_sex("UNKNOWN"), "UNKNOWN")

    def test_repository_creates_schema(self):
        """
        Verifies that 'countries' and 'health_facts' tables are created on init.
        """
        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()
        
        tables = ["countries", "health_facts"]
        for table in tables:
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}';")
            self.assertIsNotNone(cursor.fetchone(), f"Table {table} missing")
        conn.close()

    def test_persist_and_query_health_data(self):
        """
        Tests the full flow:
        1. Insert Country Reference Data.
        2. Insert Health Fact.
        3. Query joined data by year.
        """
        # 1. Store Reference Data
        self.repo.upsert_country(code="FRA", name="France", region="Europe")
        
        # 2. Store Transactional Data
        self.repo.insert_health_fact(
            country_code="FRA",
            year=2021,
            sex="Male",
            value=82.5,
            indicator="Life Expectancy"
        )
        
        # 3. Retrieve View Model
        results = self.repo.fetch_facts_by_year(2021)
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['country'], "France")
        self.assertEqual(results[0]['value'], 82.5)

if __name__ == '__main__':
    unittest.main()