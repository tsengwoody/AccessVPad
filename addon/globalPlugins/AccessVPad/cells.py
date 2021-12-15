class Char:
	def __init__(self, data):
		self._value = data[0]

	@property
	def value(self):
		return self._value

	@value.setter
	def value(self, value):
		self._value = value[0]

class Str:
	def __init__(self, data):
		self._value = data

	@property
	def value(self):
		return self._value

	@value.setter
	def value(self, value):
		self._value = value
