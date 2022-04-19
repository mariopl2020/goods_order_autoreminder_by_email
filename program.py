"""Contains main functions of program and defines its working"""
from database_manager import Database


class Program():
	"""Represents program responsible for basic database management of raw material stocks and sending email's
	reminders when stock is too low and needed to be reviewed"""

	def __init__(self):
		"""Initiates new program object"""

		self.database = Database()

	def main_run(self):
		"""Collects methods to create core of program run"""

		self.database.define_parser_arguments()
		if self.database.parsed_arguments.create_db:
			self.database.check_database_existence()
			self.database.create_new_database()


