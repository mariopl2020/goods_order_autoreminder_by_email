"""Collects database_manager module's tests"""
import pytest
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


def test_create_raw_materials_table():
    """Checks if method correctly created empty table in database"""

    #GIVEN
    test_database = Database(":memory:")
    expected_rows_number = 0
    expected_table_content = []
    with sqlite3.connect(test_database.path) as test_database.connection:
        test_database.cursor = test_database.connection.cursor()
        #WHEN
        test_database.create_raw_materials_table()
        test_database.cursor.execute("SELECT * FROM raw_materials_stock")
        rows_from_database = test_database.cursor.fetchall()
        print(rows_from_database)
        #THEN
        assert len(rows_from_database) == expected_rows_number
        assert rows_from_database == expected_table_content


def test_drop_table_from_database():
    """Checks if method correctly deletes table from database"""

    #GIVEN
    test_database = Database(":memory:")
    with sqlite3.connect(test_database.path) as test_database.connection:
        test_database.cursor = test_database.connection.cursor()
        test_database.create_raw_materials_table()
        test_database.show_data()
        test_database.drop_table_from_database()
        #WHEN
        with pytest.raises(sqlite3.OperationalError) as exception:
            test_database.show_data()
            #THEN
            assert exception == "no such table: raw_materials_stock"


def test_add_sample_raw_materials_stocks():
    """Checks if method correctly adds sample rows to database table"""

    #GIVEN
    test_database = Database(":memory:")
    expected_rows_number = 4
    expected_table_content = [(1, '22REW', 345721, 1000, 7.89, '2022-04-19', 'testuser@domain.com'),
                              (2, '32REW', 345718, 2000, 4.2, '2022-04-20', 'testuser2@domain.com'),
                              (3, 'BYSE', 345719, 10000, 3, '2022-04-20', 'testuser2@domain.com'),
                              (4, 'OILB', 345729, 1740, 11.4, '2022-04-20', 'testuser3@domain.com')]
    with sqlite3.connect(test_database.path) as test_database.connection:
        test_database.cursor = test_database.connection.cursor()
        test_database.create_raw_materials_table()
        #WHEN
        test_database.add_sample_raw_materials_stocks()
        test_database.cursor.execute("SELECT * FROM raw_materials_stock")
        rows_from_database = test_database.cursor.fetchall()
        #THEN
        assert len(rows_from_database) == expected_rows_number
        assert rows_from_database == expected_table_content









