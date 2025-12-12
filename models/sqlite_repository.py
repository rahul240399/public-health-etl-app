import sqlite3

class SqliteHealthRepository:
    """
    Manages data persistence using a SQLite Schema.
    """

    def __init__(self, db_path="health_data.db"):
        self.db_path = db_path
        self._initialize_database()

    def _get_connection(self):
        """Opens a connection, enables Foreign Keys, and sets row factory."""
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON") # Enforce Foreign Key constraints
        conn.row_factory = sqlite3.Row
        return conn

    def close_connection(self):
        """Safe shutdown hook."""
        pass

    def _initialize_database(self):
        """Creates the Schema tables if they do not exist."""
        with self._get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS countries (
                    code TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    region TEXT
                )
            ''')
            
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
        Idempotent Operation: Inserts or Updates country data.
        Prevents duplicate key errors.
        """
        with self._get_connection() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO countries (code, name, region) VALUES (?, ?, ?)",
                (code, name, region)
            )

    def insert_health_fact(self, country_code, year, sex, value, indicator):
        """
        Transactional insert of health facts.
        Edge Case: Silently fails/logs if Foreign Key (Country) is missing.
        """
        try:
            with self._get_connection() as conn:
                conn.execute('''
                    INSERT INTO health_facts (country_code, year, sex, value, indicator)
                    VALUES (?, ?, ?, ?, ?)
                ''', (country_code, year, sex, value, indicator))
        except sqlite3.IntegrityError as e:
            # Captures "FOREIGN KEY constraint failed"
            # In a real app, we might log this to a file
            print(f"[WARNING] Skipped invalid record: {e}")

    def fetch_facts_by_year(self, year):
        """
        Retrieves health facts joined with country names.
        """
        with self._get_connection() as conn:
            cursor = conn.execute('''
                SELECT f.year, c.name as country, f.sex, f.value, f.indicator
                FROM health_facts f
                JOIN countries c ON f.country_code = c.code
                WHERE f.year = ?
            ''', (year,))
            return [dict(row) for row in cursor.fetchall()]