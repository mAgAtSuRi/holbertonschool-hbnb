from abc import ABC
import uuid
from datetime import datetime


class Base(ABC):
	"""Abstract class giving a unique id and
	the created and updated time of an object"""
	def __init__(self):
		self.id = str(uuid.uuid4())
		self.created_at = datetime.now()
		self.updated_at = datetime.now()

	def save(self):
		"Update the updated_at whenever the object is modified."
		self.updated_at = datetime.now()
	
	def update(self, data):
		"Update the attributes of the object"
		"based on the provided dictionary"
		for key, value in data.items():
			if hasattr(self, key):
				setattr(self, key, value)
		self.save()