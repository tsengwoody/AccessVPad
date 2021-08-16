import textInfos

class PlaneWindowTextInfo(textInfos.offsets.OffsetsTextInfo):
	def __init__(self, obj, position):
		super().__init__(obj, position)
		self.obj = obj

	def _getStoryLength(self):
		data = self.obj.data.data
		serializes = ""
		for y_row in data:
			for x_cell in y_row:
				serializes += x_cell.value
			serializes += "\n"
		return len(serializes)

	def _getStoryText(self):
		"""Retrieve the entire text of the object.
		@return: The entire text of the object.
		@rtype: unicode
		"""
		data = self.obj.data.data
		serializes = ""
		for y_row in data:
			for x_cell in y_row:
				serializes += x_cell.value
			serializes += "\n"
		return serializes

	def _getTextRange(self, start, end):
		"""Retrieve the text in a given offset range.
		@param start: The start offset.
		@type start: int
		@param end: The end offset (exclusive).
		@type end: int
		@return: The text contained in the requested range.
		@rtype: unicode
		"""
		text = self._getStoryText()
		return text[start:end] if text else ""

class TableWindowTextInfo(textInfos.offsets.OffsetsTextInfo):
	def __init__(self, obj, position):
		super().__init__(obj, position)
		self.obj = obj

	def _getStoryLength(self):
		data = self.obj.data.pointcell.value
		serializes = data
		return len(serializes)

	def _getStoryText(self):
		"""Retrieve the entire text of the object.
		@return: The entire text of the object.
		@rtype: unicode
		"""
		data = self.obj.data.pointcell.value
		serializes = data
		return serializes

	def _getTextRange(self, start, end):
		"""Retrieve the text in a given offset range.
		@param start: The start offset.
		@type start: int
		@param end: The end offset (exclusive).
		@type end: int
		@return: The text contained in the requested range.
		@rtype: unicode
		"""
		text = self._getStoryText()
		return text[start:end] if text else ""

class TreeWindowTextInfo(textInfos.offsets.OffsetsTextInfo):
	def __init__(self, obj, position):
		super().__init__(obj, position)
		self.obj = obj

	def _getStoryLength(self):
		data = self.obj.data.pointer.label
		serializes = data
		return len(serializes)

	def _getStoryText(self):
		"""Retrieve the entire text of the object.
		@return: The entire text of the object.
		@rtype: unicode
		"""
		data = self.obj.data.pointer.label
		serializes = data
		return serializes

	def _getTextRange(self, start, end):
		"""Retrieve the text in a given offset range.
		@param start: The start offset.
		@type start: int
		@param end: The end offset (exclusive).
		@type end: int
		@return: The text contained in the requested range.
		@rtype: unicode
		"""
		text = self._getStoryText()
		return text[start:end] if text else ""

class GraphWindowTextInfo(textInfos.offsets.OffsetsTextInfo):
	def __init__(self, obj, position):
		super().__init__(obj, position)
		self.obj = obj

	def _getStoryLength(self):
		try:
			data = self.obj.data.pointer.label
		except:
			data = ""
		serializes = data
		return len(serializes)

	def _getStoryText(self):
		"""Retrieve the entire text of the object.
		@return: The entire text of the object.
		@rtype: unicode
		"""
		try:
			data = self.obj.data.pointer.label
		except:
			data = ""
		serializes = data
		return serializes

	def _getTextRange(self, start, end):
		"""Retrieve the text in a given offset range.
		@param start: The start offset.
		@type start: int
		@param end: The end offset (exclusive).
		@type end: int
		@return: The text contained in the requested range.
		@rtype: unicode
		"""
		text = self._getStoryText()
		return text[start:end] if text else ""
