class InvalidMenuNumber(Exception):
	"""Exception to be raised when user input not existing menu option number"""

	def __init__(self, text):
		"""Initiation of object"""

		super().__init__(text)
