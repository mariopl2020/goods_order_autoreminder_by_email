import datetime

from freezegun import freeze_time
from mock import mock
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
        test_database.get_all_materials()
        test_database.drop_table_from_database()
        #WHEN
        with pytest.raises(sqlite3.OperationalError) as exception:
            test_database.get_all_materials()
            #THEN
            assert exception == "no such table: raw_materials_stock"


def test_add_sample_raw_materials_stocks():
    """Checks if method correctly adds sample rows to database table"""

    #GIVEN
    test_database = Database(":memory:")
    expected_rows_number = 4
    expected_table_content = [(1, '22REW', 345721, 1000, 7.89, '2022-04-19', 'testuser@domain.com'),
                              (2, '32REW', 345718, 2000, 4.2, '2022-04-18', 'testuser2@domain.com'),
                              (3, 'BYSE', 345719, 10000, 3, '2022-04-17', 'testuser2@domain.com'),
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


def test_get_all_materials():
    """"""

    #GIVEN
    test_database = Database(":memory:")
    with sqlite3.connect(test_database.path) as test_database.connection:
        test_database.cursor = test_database.connection.cursor()
        test_database.create_raw_materials_table()
        test_database.add_sample_raw_materials_stocks()
    expected_materials = [(1, '22REW', 345721, 1000, 7.89, '2022-04-19', 'testuser@domain.com'),
                          (2, '32REW', 345718, 2000, 4.2, '2022-04-18', 'testuser2@domain.com'),
                          (3, 'BYSE', 345719, 10000, 3, '2022-04-17', 'testuser2@domain.com'),
                          (4, 'OILB', 345729, 1740, 11.4, '2022-04-20', 'testuser3@domain.com')]
    #WHEN
    materials = test_database.get_all_materials()
    #THEN
    assert materials == expected_materials


@freeze_time(datetime.date(2022, 4, 21))
def test_get_materials_to_review():
    """Checks if method returns correct list of materials where difference between today and last review date
    is equal or greater than standard - 3 days. Used wrapper to freeze variable indicates today in testcase"""

    # GIVEN
    test_database = Database(":memory:")
    expected_materials_return = [(2, '32REW', 345718, 2000, 4.2, '2022-04-18', 'testuser2@domain.com'),
                                 (3, 'BYSE', 345719, 10000, 3, '2022-04-17', 'testuser2@domain.com')]
    with sqlite3.connect(test_database.path) as test_database.connection:
        test_database.cursor = test_database.connection.cursor()
        test_database.create_raw_materials_table()
        test_database.add_sample_raw_materials_stocks()
    # WHEN
    materials_to_review = test_database.get_materials_to_review(days_interval=3)
    # THEN
    assert materials_to_review == expected_materials_return


@freeze_time(datetime.date(2022, 4, 21))
def test_get_materials_to_review_shortened_days_interval():
    """Checks if method returns correct list of materials where difference beetween today and last review date
    is equal or greater than indicated 2 days. Used wrapper to freeze variable indicates today in testcase"""

    # GIVEN
    test_database = Database(":memory:")
    expected_materials_return = [(1, '22REW', 345721, 1000, 7.89, '2022-04-19', 'testuser@domain.com'),
                                 (2, '32REW', 345718, 2000, 4.2, '2022-04-18', 'testuser2@domain.com'),
                                 (3, 'BYSE', 345719, 10000, 3, '2022-04-17', 'testuser2@domain.com')]
    with sqlite3.connect(test_database.path) as test_database.connection:
        test_database.cursor = test_database.connection.cursor()
        test_database.create_raw_materials_table()
        test_database.add_sample_raw_materials_stocks()
    # WHEN
    materials_to_review = test_database.get_materials_to_review(days_interval=2)
    # THEN
    assert materials_to_review == expected_materials_return








