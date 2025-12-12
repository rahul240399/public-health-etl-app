import sqlite3

class SqliteHealthRepository:
    """
    Manages data persistence using a SQLite Star Schema.
    Handles connections, schema creation, and SQL execution.
    """

    def __init__(self, db_path="health_data.db"):
        self.db_path = db_path
        self._initialize_database()

    def _get_connection(self):
        """
        Opens a connection and configures row_factory for dict-like access.
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def close_connection(self):
        """
        Placeholder for connection cleanup if connection pooling is added.
        """
        pass

    def _initialize_database(self):
        """
        Creates the 'countries' and 'health_facts' tables if they do not exist.
        """
        with self._get_connection() as conn:
            # Dimension Table (Reference Data)
            conn.execute('''
                CREATE TABLE IF NOT EXISTS countries (
                    code TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    region TEXT
                )
            ''')
            
            # Fact Table (Transactional Data)
            conn.execute('''
                CREATE TABLE IF NOT EXISTS health_facts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    country_code TEXT,
                    year INTEGER,
                    sex TEXT,
                    value REAL,
                    indicator TEXT,
                    FOREIGN KEY (country_code) REFERENCES countries (code)
                )
            ''')

    def upsert_country(self, code, name, region="Unknown"):
        """
        Inserts a new country or updates it if the code already exists.
        """
        with self._get_connection() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO countries (code, name, region) VALUES (?, ?, ?)",
                (code, name, region)
            )

    def insert_health_fact(self, country_code, year, sex, value, indicator):
        """
        Inserts a single health data record into the fact table.
        """
        with self._get_connection() as conn:
            conn.execute('''
                INSERT INTO health_facts (country_code, year, sex, value, indicator)
                VALUES (?, ?, ?, ?, ?)
            ''', (country_code, year, sex, value, indicator))

    def fetch_facts_by_year(self, year):
        """
        Retrieves health facts joined with country names for a specific year.
        Returns a list of dictionary-like Row objects.
        """
        with self._get_connection() as conn:
            cursor = conn.execute('''
                SELECT f.year, c.name as country, f.sex, f.value, f.indicator
                FROM health_facts f
                JOIN countries c ON f.country_code = c.code
                WHERE f.year = ?
            ''', (year,))
            return [dict(row) for row in cursor.fetchall()]