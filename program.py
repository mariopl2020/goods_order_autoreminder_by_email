"""Contains main functions of program and defines its working"""
import smtplib
from smtplib import SMTPAuthenticationError
import sys
from database_manager import Database
from exceptions.program_exceptions import InvalidMenuNumber
from mail_manager import Email


class Program():
    """Represents program responsible for basic database management of raw material stocks
    and sending email's reminders when stock is too low and needed to be reviewed"""

    def __init__(self):
        """Initiates new program object"""

        self.database = Database()
        self.email = Email()
        self.menu_actions = {
            1: {
                "description": "Show raw materials to be reviewed",
                "actions": [
                    {
                        "action_method": self.database.show_data,
                        "argument": self.database.get_materials_to_review,
                    },
                ]
            },
            2: {
                "description": "Send autoreminders about stock review",
                "actions": [
                    {
                        "action_method": self.send_email_reminders,
                        "argument": None,
                    },
                ]
            },
            3: {
                "description": "Show all raw materials",
                "actions": [
                    {
                        "action_method": self.database.show_data,
                        "argument": self.database.get_all_materials,
                    },
                ]
            },
            4: {
                "description": "Add single material to database",
                "actions": [
                    {
                        "action_method": self.database.add_new_material,
                        "argument": None,
                    },
                ]
            },
            5: {
                "description": "Change stock of chosen material",
                "actions": [
                    {
                        "action_method": self.database.change_current_stock,
                        "argument": None,
                    },
                ]
            },
            6: {
                "description": "Add sample raw materials to database",
                "actions": [
                    {
                        "action_method": self.database.add_sample_raw_materials_stocks,
                        "argument": None,
                    },
                ]
            },
            7: {
                "description": "Reset database",
                "actions": [
                    {
                        "action_method": self.database.reset_database,
                        "argument": None,
                    },
                ]
            },
            0: {
                "description": "Quit program",
                "actions": [
                    {
                        "action_method": self.database.disconnect_database,
                        "argument": None,
                    },
                    {
                        "action_method": sys.exit,
                        "argument": None,
                    },
                ]
            }
        }

    def print_menu(self):
        """Prints main menu of program as list of available options to be performed"""

        print("Menu")
        for key, option in self.menu_actions.items():
            print(f"{key}. {option['description']}", end="\t")
            if key % 3 == 0:
                print()

    def main_run(self):
        """Collects methods creating core of program run"""

        self.database.define_parser_arguments()
        self.database.start_database()
        if self.database.parsed_arguments.add:
            self.database.add_new_material()
        self.select_menu_options()

    @staticmethod
    def fill_message_template(material_name, stock, last_review_date):
        """Creates personalized email content to be sent as reminder

        Arguments:
            material_name (str): name of material
            stock (str): stock level [kg]
            last_review_date (str): date of last stock review

        Returns:
            message (str): complete email message content to be sent"""

        sender = "System alert"
        subject = f"Raw material {material_name} needs review"
        body = f"Reminder!\n Raw material {material_name} has {stock} kg " \
               f"stock and was reviewed last time on {last_review_date}"

        message = f"From: {sender}\n" \
                  f"Subject: {subject}\n" \
                  f"{body}"

        return message

    def send_email_reminders(self):
        """Allows sending reminding emails to responsible persons where raw materials
        have too long time with no review"""

        with smtplib.SMTP_SSL(host=self.email.smtp_server, port=self.email.smtp_port)\
                as self.email.server:
            try:
                self.email.log_to_admin_email()
                print("Logging successfully")
                materials_list = self.database.get_materials_to_review()
                for material in materials_list:
                    material_name = material.sku_description
                    stock = material.current_stock_kg
                    last_review_date = material.last_review_date
                    email_address = material.responsible_employee
                    message = self.fill_message_template(material_name, stock, last_review_date)
                    self.email.send_email(mail_to=email_address, msg_content=message)
            except SMTPAuthenticationError:
                print("Entered incorrect password")

    def select_menu_options(self):
        """Creates option path of program functions and allows user to decide which ones
        will be performed."""

        while True:
            self.print_menu()
            try:
                choice = int(input("Select operation:\n"))
                if choice not in self.menu_actions.keys():
                    raise InvalidMenuNumber("Wrong number entered. Try again\n" + "-" * 40)
            except ValueError:
                print("Wrong value entered. Try again\n" + "-" * 40)
                continue
            except InvalidMenuNumber as exception:
                print(exception)
                continue
            for action in self.menu_actions[choice]["actions"]:
                argument_func = action["argument"]
                if argument_func is None:
                    action["action_method"]()
                else:
                    argument = argument_func()
                    action["action_method"](argument)
