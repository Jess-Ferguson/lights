class DatabaseException(Exception):
	"""
	Base class for exceptions in the database
	"""
	def __init__(self, message, payload = None):
		self.message = message
		self.payload = payload
	def __str__(self):
		return str(self.message)