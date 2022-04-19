"""Collects database_manager module's tests"""
from database_manager import Database


def test_check_data_base_existence_positive():
	"""Tests method if checking database's existing works correct. Case where database exists"""

	#GIVEN
	database_path = "tests/data/test_base.db"
	test_database = Database(database_path)
	test_database.create_new_database()
	#WHEN
	database_exists = test_database.check_database_existence()
	#THEN
	assert database_exists == True


def test_check_data_base_existence_negative():
	"""Tests method if checking database's existing works correct. Case where database exists"""

	#GIVEN
	database_path = "tests/data/not_existing_base.db"
	test_database = Database(database_path)
	#WHEN
	database_exists = test_database.check_database_existence()
	#THEN
	assert database_exists == False


