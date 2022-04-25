"""Contains functionalities to manage and works with administrator email account"""


class Email():
	"""Represents email account"""

	def __init__(self):
		"""Initiates email account"""
		self.admin_email = "autoadmfactor@gmail.com"
		self.smtp_server = "smtp.gmail.com"
		self.smtp_port = 465
		self.server = None

	def log_to_admin_email(self):
		"""Allows administrator to login into his account."""

		admin_password = input("Enter your email password\n")
		self.server.login(user=self.admin_email, password=admin_password)

	def send_email(self, mail_to, msg_content):
		"""Sends mail from admin email account to chosen address with parametrized content

		Arguments:
			mail_to (str): email address what will be receiver of message
			msg_content (str): message content"""

		self.server.sendmail(from_addr=self.admin_email, to_addrs=mail_to, msg=msg_content)

	def logout(self):
		"""Ends connection with administrator's email server"""

		self.server.close()
