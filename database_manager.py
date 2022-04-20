"""Includes class connected with database operations"""
from argparse import ArgumentParser
import os
import sqlite3
import datetime


class Database():
    """Represents database of raw material stocks"""

    def __init__(self, path="data/goods_database.db"):
        """Initiates database object"""

        self.exists = False
        self.path = path
        self.parsed_arguments = None
        self.cursor = None
        self.connection = None

    def define_parser_arguments(self):
        """Defines arguments connected with database as flags able to trigger when program is calling"""

        argument_parser = ArgumentParser()
        argument_parser.add_argument("--reset_db",
                                     help="Create new database",
                                     action="store_true")
        argument_parser.add_argument("--add",
                                     help="Add new raw material",
                                     action="store_true")
        self.parsed_arguments = argument_parser.parse_args()

    def check_database_existence(self):
        """Checks if database with provided path exists"""

        self.exists = os.path.exists(self.path)

    def connect_database(self):
        """Creates new database connection"""

        with sqlite3.connect(self.path) as self.connection:
            self.cursor = self.connection.cursor()

    def drop_table_from_database(self):
        """Drops existing table from database"""

        self.cursor.execute("DROP TABLE raw_materials_stock")

    def create_raw_materials_table(self):
        """Creates initial table of raw materials"""

        self.cursor.execute("CREATE TABLE raw_materials_stock (id INTEGER PRIMARY KEY AUTOINCREMENT,"
                            " sku_description TEXT, sku_id INTEGER, current_stock_kg NUMERIC,"
                            " price NUMERIC, last_review_date DATE, responsible_employee TEXT)")

    def start_database(self):
        """Starts database if it exists, not or is restarted"""

        self.check_database_existence()
        self.connect_database()
        if self.parsed_arguments.reset_db:
            if self.exists:
                self.drop_table_from_database()
            self.create_raw_materials_table()
        elif not self.exists:
            self.create_raw_materials_table()

    def add_new_material(self):
        """Adds new row to raw material's table"""

        sku_description = input("Enter raw material name\n")
        sku_id = input("Enter material sku code\n")
        current_stock_kg = float(input("Enter current stock in kg\n"))
        price = float(input("Enter material unit price\n"))
        last_review_date = datetime.date.today()
        responsible_employee = input("Enter person email responsible for material's management\n")
        self.cursor.execute("INSERT INTO raw_materials_stock"
                            "(sku_description,"
                            "sku_id,"
                            "current_stock_kg,"
                            "price,"
                            "last_review_date,"
                            "responsible_employee)"
                            "VALUES(?, ?, ?, ?, ?, ?)",
                            (sku_description, sku_id, current_stock_kg, price,
                             last_review_date, responsible_employee))
        self.connection.commit()

    # @TODO changing stocks by hand
    # @TODO show database

    def add_sample_raw_materials_stocks(self):
        """"""

        pass
