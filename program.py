"""Contains main functions of program and defines its working"""
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
                            1: "Add single material to database",
                            2: "Show all raw materials",
                            3: "Add sample raw materials stock into your database",
                            4: "Show raw materials to be reviewed",
                            5: "Change stock of chosen material",
                            6: "Send autoreminders about stock review",
                            9: "Reset database",
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
        self.database.disconnect_database()

    def send_reminders_emails(self):
        """Allows sending reminding emails to responsible persons where raw materials have too long time
        with no review"""

        # @TODO to develop
        self.email.log_to_admin_email()
        # self.get_emails_to_send()
        self.email.send_email()
        self.email.logout()

    def select_menu_options(self):
        """Creates option path of program functions and allows user to decide which ones
        will be performed."""

        while True:
            self.print_menu()
            try:
                choice = int(input("Select operation:\n"))
                if choice not in self.menu_content.keys():
                    raise InvalidMenuNumber("Wrong number entered. Try again\n" + "-"*40)
            except ValueError:
                print("Wrong value entered. Try again\n"+"-"*40)
                continue
            except InvalidMenuNumber as exception:
                print(exception)
                continue
            if choice == 1:
                self.database.add_new_material()
            elif choice == 2:
                all_materials = self.database.get_all_materials()
                self.database.show_data(all_materials)
            elif choice == 3:
                self.database.add_sample_raw_materials_stocks()
            elif choice == 4:
                materials_to_review = self.database.get_materials_to_review()
                self.database.show_data(materials_to_review)
            elif choice == 5:
                try:
                    self.database.change_current_stock()
                except NotExistingSKU as exception:
                    print(exception)
            elif choice == 6:
                # @TODO
                self.send_reminders_emails()
            elif choice == 9:
                self.database.reset_database()
            elif choice == 0:
                exit()
            print("-"*40)




