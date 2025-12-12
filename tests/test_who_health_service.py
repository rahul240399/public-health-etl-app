import unittest
import os
import sys

# Add parent directory to path to allow module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.sqlite_repository import SqliteHealthRepository
from models.who_code_normalizer import WhoCodeNormalizer

class TestWhoHealthService(unittest.TestCase):
    
    def setUp(self):
        """Sets up a fresh database environment before each test."""
        print("\n--- Starting Test ---")
        self.test_db_path = "test_edge_cases.db"
        self.repo = SqliteHealthRepository(self.test_db_path)

    def tearDown(self):
        """Cleans up the database file after test execution."""
        self.repo.close_connection()
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
        print("--- Test Finished ---\n")

    def test_normalizer_edge_cases(self):
        """Verifies that the normalizer handles None, empty strings, and whitespace."""
        # Case 1: None Input
        print("[ACTION] Normalizing 'None' input...")
        result_none = WhoCodeNormalizer.normalize_sex(None)
        print(f"[ASSERT] Result should be None... (Got: {result_none})")
        self.assertIsNone(result_none)

        # Case 2: Empty String
        print("[ACTION] Normalizing empty string input...")
        result_empty = WhoCodeNormalizer.normalize_sex("")
        print(f"[ASSERT] Result should be empty string... (Got: '{result_empty}')")
        self.assertEqual(result_empty, "")

        # Case 3: Whitespace Only
        print("[ACTION] Normalizing whitespace input '   '...")
        result_space = WhoCodeNormalizer.normalize_sex("   ")
        print(f"[ASSERT] Result should be preserved as '   '... (Got: '{result_space}')")
        self.assertEqual(result_space, "   ")

    def test_normalizer_type_safety(self):
        """Verifies that the system handles unexpected data types safely."""
        # Case: Integer Input where String expected
        print("[ACTION] Passing integer 123 to string normalizer...")
        result_int = WhoCodeNormalizer.normalize_sex(123)
        
        print(f"[ASSERT] System should return input without crashing... (Got: {result_int})")
        self.assertEqual(result_int, 123)

    def test_repository_idempotency(self):
        """Verifies that inserting the same country twice does not cause duplicates or crashes."""
        print("[ACTION] Upserting Country 'FRA' (First Attempt)...")
        self.repo.upsert_country("FRA", "France", "Europe")
        
        print("[ACTION] Upserting Country 'FRA' (Second Attempt - Duplicate)...")
        self.repo.upsert_country("FRA", "France", "Europe")

        # Verify logic: Should still be 1 record, logic handles the conflict
        # We need a direct SQL check here to verify state
        import sqlite3
        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT count(*) FROM countries WHERE code='FRA'")
        count = cursor.fetchone()[0]
        conn.close()

        print(f"[ASSERT] Country count should be 1... (Got: {count})")
        self.assertEqual(count, 1)

    def test_repository_integrity_foreign_keys(self):
        """Verifies that adding health data for a missing country fails gracefully (or is skipped)."""
        print("[ACTION] Attempting to insert health record for non-existent country 'ZZZ'...")
        
        # Note: 'ZZZ' has not been added to the countries table.
        # The repository should handle the SQLite IntegrityError internally.
        self.repo.insert_health_fact(
            country_code="ZZZ",
            year=2022,
            sex="Male",
            value=50.0,
            indicator="Test"
        )

        # Verify: The fact should NOT be saved because the parent Country is missing
        results = self.repo.fetch_facts_by_year(2022)
        print(f"[ASSERT] Result list should be empty (Foreign Key Constraint)... (Got len: {len(results)})")
        self.assertEqual(len(results), 0)

if __name__ == '__main__':
    unittest.main()