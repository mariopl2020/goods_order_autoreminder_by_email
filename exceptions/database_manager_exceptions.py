class NotExistingSKU(Exception):
	"""Kind of exception what is raised when user input SKU what does not
	exist in database"""

	def __init__(self, text):
		"""Initiation of object"""

		super().__init__(text)