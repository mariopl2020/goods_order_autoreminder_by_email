"""Contains tests for database manager module"""
import builtins
import datetime
from freezegun import freeze_time
import pytest
import sqlite3
from database_manager import Database
from exceptions.database_manager_exceptions import NotExistingSKU


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

    # GIVEN
    test_database = Database(":memory:")
    expected_rows_number = 0
    expected_table_content = []
    with sqlite3.connect(test_database.path) as test_database.connection:
        test_database.cursor = test_database.connection.cursor()
        # WHEN
        test_database.create_raw_materials_table()
        test_database.cursor.execute("SELECT * FROM raw_materials_stock")
        rows_from_database = test_database.cursor.fetchall()
        print(rows_from_database)
        # THEN
        assert len(rows_from_database) == expected_rows_number
        assert rows_from_database == expected_table_content


def test_drop_table_from_database():
    """Checks if method correctly deletes table from database"""

    # GIVEN
    test_database = Database(":memory:")
    with sqlite3.connect(test_database.path) as test_database.connection:
        test_database.cursor = test_database.connection.cursor()
        test_database.create_raw_materials_table()
        test_database.get_all_materials()
        test_database.drop_table_from_database()
        # WHEN
        with pytest.raises(sqlite3.OperationalError) as exception:
            test_database.get_all_materials()
            # THEN
            assert exception == "no such table: raw_materials_stock"


def test_add_sample_raw_materials_stocks():
    """Checks if method correctly adds sample rows to database table"""

    # GIVEN
    test_database = Database(":memory:")
    expected_rows_number = 4
    expected_table_content = [(1, '22REW', 345721, 1000, 7.89, '2022-04-19', 'autoadmfactor@gmail.com'),
                              (2, '32REW', 345718, 2000, 4.2, '2022-04-18', 'adampolakfactor@gmail.com'),
                              (3, 'BYSE', 345719, 10000, 3, '2022-04-17', 'autoadmfactor@gmail.com'),
                              (4, 'OILB', 345729, 1740, 11.4, '2022-04-20', 'adampolakfactor@gmail.com')]
    with sqlite3.connect(test_database.path) as test_database.connection:
        test_database.cursor = test_database.connection.cursor()
        test_database.create_raw_materials_table()
        # WHEN
        test_database.add_sample_raw_materials_stocks()
        test_database.cursor.execute("SELECT * FROM raw_materials_stock")
        rows_from_database = test_database.cursor.fetchall()
        # THEN
        assert len(rows_from_database) == expected_rows_number
        assert rows_from_database == expected_table_content


def test_get_all_materials():
    """Checks if method returns from database table all rows in correct form"""

    # GIVEN
    test_database = Database(":memory:")
    with sqlite3.connect(test_database.path) as test_database.connection:
        test_database.cursor = test_database.connection.cursor()
        test_database.create_raw_materials_table()
        test_database.add_sample_raw_materials_stocks()
    expected_materials = [(1, '22REW', 345721, 1000, 7.89, '2022-04-19', 'autoadmfactor@gmail.com'),
                          (2, '32REW', 345718, 2000, 4.2, '2022-04-18', 'adampolakfactor@gmail.com'),
                          (3, 'BYSE', 345719, 10000, 3, '2022-04-17', 'autoadmfactor@gmail.com'),
                          (4, 'OILB', 345729, 1740, 11.4, '2022-04-20', 'adampolakfactor@gmail.com')]
    # WHEN
    materials = test_database.get_all_materials()
    # THEN
    assert materials == expected_materials


@freeze_time(datetime.date(2022, 4, 21))
def test_get_materials_to_review():
    """Checks if method returns correct list of materials where difference between today and last review date
    is equal or greater than standard - 3 days. Used wrapper to freeze variable indicates today in testcase"""

    # GIVEN
    test_database = Database(":memory:")
    expected_materials_return = [(2, '32REW', 345718, 2000, 4.2, '2022-04-18', 'adampolakfactor@gmail.com'),
                                 (3, 'BYSE', 345719, 10000, 3, '2022-04-17', 'autoadmfactor@gmail.com')]
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
    expected_materials_return = [(1, '22REW', 345721, 1000, 7.89, '2022-04-19', 'autoadmfactor@gmail.com'),
                                 (2, '32REW', 345718, 2000, 4.2, '2022-04-18', 'adampolakfactor@gmail.com'),
                                 (3, 'BYSE', 345719, 10000, 3, '2022-04-17', 'autoadmfactor@gmail.com')]
    with sqlite3.connect(test_database.path) as test_database.connection:
        test_database.cursor = test_database.connection.cursor()
        test_database.create_raw_materials_table()
        test_database.add_sample_raw_materials_stocks()
    # WHEN
    materials_to_review = test_database.get_materials_to_review(days_interval=2)
    # THEN
    assert materials_to_review == expected_materials_return


@freeze_time(datetime.date(2022, 4, 21))
def test_change_current_stock_correct_run():
    """Checks if method correctly change stock for provided, existing material and automatically set current date"""

    # GIVEN
    expected_materials_return = [(1, '22REW', 345721, 300, 7.89, '2022-04-21', 'autoadmfactor@gmail.com'),
                                 (2, '32REW', 345718, 2000, 4.2, '2022-04-18', 'adampolakfactor@gmail.com'),
                                 (3, 'BYSE', 345719, 10000, 3, '2022-04-17', 'autoadmfactor@gmail.com'),
                                 (4, 'OILB', 345729, 1740, 11.4, '2022-04-20', 'adampolakfactor@gmail.com')]
    input_values = ["345721", "300"]
    test_database = Database(":memory:")
    with sqlite3.connect(test_database.path) as test_database.connection:
        test_database.cursor = test_database.connection.cursor()
        test_database.create_raw_materials_table()
        test_database.add_sample_raw_materials_stocks()

        def mock_input(input_text):
            return input_values.pop(0)

        builtins.input = mock_input
        # WHEN
        test_database.change_current_stock()
        print(test_database.get_all_materials())
    # THEN
    assert test_database.get_all_materials() == expected_materials_return


def test_change_current_stock_text_as_sku():
    """Checks if provided sku as string is handled as exception and does not change anything in database"""

    # GIVEN
    expected_materials_return = [(1, '22REW', 345721, 1000, 7.89, '2022-04-19', 'autoadmfactor@gmail.com'),
                                 (2, '32REW', 345718, 2000, 4.2, '2022-04-18', 'adampolakfactor@gmail.com'),
                                 (3, 'BYSE', 345719, 10000, 3, '2022-04-17', 'autoadmfactor@gmail.com'),
                                 (4, 'OILB', 345729, 1740, 11.4, '2022-04-20', 'adampolakfactor@gmail.com')]
    input_values = ["zero", 20]
    test_database = Database(":memory:")
    with sqlite3.connect(test_database.path) as test_database.connection:
        test_database.cursor = test_database.connection.cursor()
        test_database.create_raw_materials_table()
        test_database.add_sample_raw_materials_stocks()

        def mock_input(input_text):
            return input_values.pop(0)

        builtins.input = mock_input
        # WHEN
        test_database.change_current_stock()
        # THEN
        assert test_database.get_all_materials() == expected_materials_return


def test_change_current_stock_number_not_sku():
    """Checks if provided number as sku not existing in database causes exception raising
    and does not change anything in base"""

    # GIVEN
    expected_materials_return = [(1, '22REW', 345721, 1000, 7.89, '2022-04-19', 'autoadmfactor@gmail.com'),
                                 (2, '32REW', 345718, 2000, 4.2, '2022-04-18', 'adampolakfactor@gmail.com'),
                                 (3, 'BYSE', 345719, 10000, 3, '2022-04-17', 'autoadmfactor@gmail.com'),
                                 (4, 'OILB', 345729, 1740, 11.4, '2022-04-20', 'adampolakfactor@gmail.com')]
    input_values = [222, 2000]
    test_database = Database(":memory:")
    with sqlite3.connect(test_database.path) as test_database.connection:
        test_database.cursor = test_database.connection.cursor()
        test_database.create_raw_materials_table()
        test_database.add_sample_raw_materials_stocks()

        def mock_input(input_text):
            return input_values.pop(0)

        builtins.input = mock_input
        # WHEN
        with pytest.raises(NotExistingSKU):
            test_database.change_current_stock()
        # THEN
        assert test_database.get_all_materials() == expected_materials_return


def test_change_current_stock_sku_ok_qty_wrong():
    """Checks if wrongly provided quantity as input does not change anything in database as expected"""

    # GIVEN
    test_database = Database(":memory:")
    user_input = [345721, "twenty"]
    expected_materials_return = [(1, '22REW', 345721, 1000, 7.89, '2022-04-19', 'autoadmfactor@gmail.com'),
                                 (2, '32REW', 345718, 2000, 4.2, '2022-04-18', 'adampolakfactor@gmail.com'),
                                 (3, 'BYSE', 345719, 10000, 3, '2022-04-17', 'autoadmfactor@gmail.com'),
                                 (4, 'OILB', 345729, 1740, 11.4, '2022-04-20', 'adampolakfactor@gmail.com')]
    with sqlite3.connect(test_database.path) as test_database.connection:
        test_database.cursor = test_database.connection.cursor()
        test_database.create_raw_materials_table()
        test_database.add_sample_raw_materials_stocks()

        def input_mock(input_text):
            return user_input.pop(0)

        builtins.input = input_mock

        # WHEN
        test_database.change_current_stock()
        # THEN
        assert test_database.get_all_materials() == expected_materials_return


def test_change_current_stock_sku_ok_qty_expected_result_wrong():
    """Checks if wrongly provided quantity is saved in database. Scenario considers wrong attitude
    that quantity is changed. Thus expected result is not equal to actual"""

    # GIVEN
    test_database = Database(":memory:")
    user_input = [345721, "twenty"]
    wrongly_expected_materials_return = [
        (1, '22REW', 345721, "twenty", 7.89, '2022-04-19', 'autoadmfactor@gmail.com'),
        (2, '32REW', 345718, 2000, 4.2, '2022-04-18', 'adampolakfactor@gmail.com'),
        (3, 'BYSE', 345719, 10000, 3, '2022-04-17', 'autoadmfactor@gmail.com'),
        (4, 'OILB', 345729, 1740, 11.4, '2022-04-20', 'adampolakfactor@gmail.com')]
    with sqlite3.connect(test_database.path) as test_database.connection:
        test_database.cursor = test_database.connection.cursor()
        test_database.create_raw_materials_table()
        test_database.add_sample_raw_materials_stocks()

        def input_mock(input_text):
            return user_input.pop(0)

        builtins.input = input_mock
        # WHEN
        test_database.change_current_stock()
        # THEN
        assert test_database.get_all_materials() != wrongly_expected_materials_return
