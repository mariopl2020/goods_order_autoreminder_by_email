"""Contains main functions of program and defines its working"""
import smtplib
from smtplib import SMTPAuthenticationError
from database_manager import Database
from exceptions.program_exceptions import InvalidMenuNumber
from exceptions.database_manager_exceptions import NotExistingSKU
from mail_manager import Email


class Program():
    """Represents program responsible for basic database management of raw material stocks and sending email's
    reminders when stock is too low and needed to be reviewed"""

    def __init__(self):
        """Initiates new program object"""

        self.database = Database()
        self.email = Email()
        self.menu_content = {
            1: "Show raw materials to be reviewed",
            2: "Send autoreminders about stock review",
            3: "Show all raw materials",
            4: "Add single material to database",
            5: "Change stock of chosen material",
            6: "Add sample raw materials to database",
            7: "Reset database",
            0: "Quit program"
        }

    def print_menu(self):
        """Prints main menu of program as list of available options to be performed"""

        print("Menu")
        for key, option in self.menu_content.items():
            print(f"{key}. {option}", end="\t")
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
        """Allows sending reminding emails to responsible persons where raw materials have too long time
        with no review"""

        with smtplib.SMTP_SSL(host=self.email.smtp_server, port=self.email.smtp_port) as self.email.server:
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
                if choice not in self.menu_content.keys():
                    raise InvalidMenuNumber("Wrong number entered. Try again\n" + "-" * 40)
            except ValueError:
                print("Wrong value entered. Try again\n" + "-" * 40)
                continue
            except InvalidMenuNumber as exception:
                print(exception)
                continue
            if choice == 1:
                materials_to_review = self.database.get_materials_to_review()
                self.database.show_data(materials_to_review)
            elif choice == 2:
                self.send_email_reminders()
            elif choice == 3:
                all_materials = self.database.get_all_materials()
                self.database.show_data(all_materials)
            elif choice == 4:
                self.database.add_new_material()
            elif choice == 5:
                try:
                    self.database.change_current_stock()
                except NotExistingSKU as exception:
                    print(exception)
            elif choice == 6:
                self.database.add_sample_raw_materials_stocks()
            elif choice == 7:
                self.database.reset_database()
            elif choice == 0:
                self.database.disconnect_database()
                exit()
            print("-" * 40)
