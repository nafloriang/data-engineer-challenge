import unittest
import sqlite3
import sys
from pathlib import Path

# Adjust sys.path to include the parent directory to access the 'app' folder.
sys.path.append(str(Path(__file__).parent.parent))

# Import utils from the 'app' directory.
from app import utils

DB_PATH = Path("C:/Users/hopem/Documents/data-engineering-challenge/mydatabase.db")
BACKUP_PATH = Path("backup.db")
AVRO_BACKUP_DIR = Path("C:/Users/hopem/Documents/data-engineering-challenge/backups")

class TestDatabaseUtils(unittest.TestCase):

    def setUp(self):
        """
        Set up method to prepare for each test.
        Insert test records into the 'departments' table.
        """
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO departments (id, department) VALUES (?, ?)", (999, 'TestDept'))
            conn.commit()

    def tearDown(self):
        """
        Tear down method after each test.
        Delete test records and any backup files created during the test.
        """
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM departments WHERE id=?", (999,))
            conn.commit()

        if BACKUP_PATH.exists():
            BACKUP_PATH.unlink()

        avro_backup = AVRO_BACKUP_DIR / "departments_backup.avro"
        if avro_backup.exists():
            avro_backup.unlink()

    def test_backup_database(self):
        """Test the database backup functionality."""
        self.assertTrue(utils.backup_database(DB_PATH), "Database backup failed.")

        self.assertTrue(BACKUP_PATH.exists(), "Backup file not found.")
        self.assertTrue((AVRO_BACKUP_DIR / "departments_backup.avro").exists(), "Avro backup file for 'departments' not found.")

    def test_restore_database(self):
        """
        Test the database restoration functionality.
        Initially, a backup is created, then the test record is deleted,
        followed by a restoration from the backup.
        """
        # First, create a backup
        self.assertTrue(utils.backup_database(DB_PATH), "Database backup failed.")

        # Now, delete the test record
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM departments WHERE id=?", (999,))
            conn.commit()

        # Restore from the backup
        self.assertTrue(utils.restore_database(BACKUP_PATH, DB_PATH), "Database restoration failed.")

        # Check if the test record is back in the database
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            result = cursor.execute("SELECT * FROM departments WHERE id=?", (999,)).fetchone()
            self.assertIsNotNone(result, "Record not restored properly.")
            self.assertEqual(result[1], 'TestDept', "Record data mismatch.")

if __name__ == '__main__':
    unittest.main()
