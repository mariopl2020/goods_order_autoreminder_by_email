"""Includes class connected with database operations"""
from argparse import ArgumentParser
from freezegun import freeze_time
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

    # @TODO make to be used also by materials to be reviewed
    def show_data(self):
        """Prints whole content of database table"""

        headers_list = ["id", "sku_description", "sku_id", "current_stock_kg", "price", "last_review_date",
                        "responsible_employee"]
        for header in headers_list:
            print(f"{header:<20}", end=" ")
        print()
        for row in self.cursor.execute("SELECT * FROM raw_materials_stock"):
            for data in row:
                print(f"{data:<20}", end=" ")
            print()

    def add_sample_raw_materials_stocks(self):
        """Adds sample rows into raw materials table in database"""

        sample_raw_materials_list = [
            ('22REW', 345721, 1000, 7.89, datetime.date(2022, 4, 19), 'testuser@domain.com'),
            ('32REW', 345718, 2000, 4.20, datetime.date(2022, 4, 18), 'testuser2@domain.com'),
            ('BYSE', 345719, 10000, 3.00, datetime.date(2022, 4, 17), 'testuser2@domain.com'),
            ('OILB', 345729, 1740, 11.40, datetime.date(2022, 4, 20), 'testuser3@domain.com')
        ]
        self.cursor.executemany("INSERT INTO raw_materials_stock"
                                "(sku_description,"
                                "sku_id,"
                                "current_stock_kg,"
                                "price,"
                                "last_review_date,"
                                "responsible_employee)"
                                "VALUES (?, ?, ?, ?, ?, ?)",
                                sample_raw_materials_list)
        self.connection.commit()

    def get_materials_to_review(self, days_interval=3):
        """Returns list of materials from database what should be reviewed in terms of stock level.
        They are indicated when days difference between review date and current date is exceeded.

         Args:
             days_interval (int): number of days what added to last review date indicates new date
             when material should be reviewed
        Returns:
            materials_to_be_reviewed (list): part of database table with materials what should be reviewed"""

        self.cursor.execute("SELECT * FROM raw_materials_stock")
        materials = self.cursor.fetchall()
        materials_to_review = []
        for material in materials:
            date = material[5]
            date_list = date.split("-")
            year = int(date_list[0])
            month = int(date_list[1])
            day = int(date_list[2])
            date = datetime.date(year, month, day)
            review_interval = datetime.timedelta(days=days_interval)
            date_to_be_reviewed = date + review_interval
            if date_to_be_reviewed <= datetime.date.today():
                materials_to_review.append(material)
        return materials_to_review




    # @TODO changing stocks by hand (includes auto date change when changed quantity)

