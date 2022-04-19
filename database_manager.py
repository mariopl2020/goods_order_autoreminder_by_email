"""Includes class connected with database operations"""
from argparse import ArgumentParser
import os
import sqlite3


class Database():
    """Represents database of raw material stocks"""

    def __init__(self, path="data/goods_database.db"):
        """Initiates database object"""

        self.path = path
        self.parsed_arguments = None

    def define_parser_arguments(self):
        """Defines arguments connected with database as flags able to trigger when program is calling"""

        argument_parser = ArgumentParser()
        argument_parser.add_argument("--create_db",
                                     help="Create new database",
                                     action="store_true")
        self.parsed_arguments = argument_parser.parse_args()

    def check_database_existence(self):
        """Checks if database with provided path exists"""

        is_database_existing = os.path.exists(self.path)
        if is_database_existing:
            return True
        else:
            return False

    def create_new_database(self):
        """Creates new database with initial table providing that such database does not exist"""

        is_database_existing = self.check_database_existence()
        if not is_database_existing:
            connection = sqlite3.connect(self.path)
            cursor = connection.cursor()
            cursor.execute("CREATE TABLE raw_materials_stock (id INTEGER PRIMARY KEY AUTOINCREMENT,"
                           " sku_description TEXT, sku_id INTEGER, current_stock_kg NUMERIC,"
                           " price NUMERIC, last_order_date DATE)")
