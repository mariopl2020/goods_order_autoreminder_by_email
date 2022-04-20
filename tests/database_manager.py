"""Collects database_manager module's tests"""
import sqlite3
from database_manager import Database


def test_check_data_base_existence_positive():
    """Tests method if checking database's existing works correct. Case where database exists"""

    # GIVEN
    database_path = "tests/data/test_base.db"
    test_database = Database(database_path)
    # WHEN
    test_database.check_database_existence()
    # THEN
    assert test_database.exists == True


def test_check_data_base_existence_negative():
    """Tests method if checking database's existing works correct. Case where database exists"""

    # GIVEN
    database_path = "tests/data/not_existing_base.db"
    test_database = Database(database_path)
    # WHEN
    test_database.check_database_existence()
    # THEN
    assert test_database.exists == False


