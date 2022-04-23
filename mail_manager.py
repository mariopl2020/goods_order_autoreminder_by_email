"""Contains functionalities to manage and works with administrator email account"""
import smtplib
from smtplib import SMTPAuthenticationError

class Email():
	"""Represents email account"""

	def __init__(self):
		"""Initiates email account"""
		self.admin_email = "autoadmfactor@gmail.com"
		self.server = None

	def log_to_admin_email(self):
		"""Connect with email server and allows administrator to login into his account.
		Protected from password correctness failure"""

		with smtplib.SMTP_SSL(host="smtp.gmail.com", port=465) as self.server:
			admin_password = input("Enter your email password\n")
			try:
				self.server.login(user=self.admin_email, password=admin_password)
				print("Logging successfully")
			except SMTPAuthenticationError:
				print("Entered incorrect password")

	# @TODO
	def send_email(self):
		""""""
		pass

	def logout(self):
		"""Ends connection with administrator's email server"""

		self.server.close()

