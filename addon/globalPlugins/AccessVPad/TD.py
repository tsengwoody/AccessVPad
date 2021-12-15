import addonHandler

from csv import reader, writer
from .cells import Char, Str

addonHandler.initTranslation()

class TDBase:
	def __init__(self, row_count, col_count):
		data = []
		for r in range(row_count):
			row = []
			for c in range(col_count):
				# row.append(self.insert_default(str((r + c)%10)))
				row.append(self.insert_default(" "))
			data.append(row)

		pointer = {"X": 0, "Y": 0}

		self.data = data
		self.pointer = pointer

	@property
	def row_count(self):
		return len(self.data)

	@property
	def col_count(self):
		return len(self.data[0])

	@property
	def linear_pos(self):
		COL_COUNT = self.col_count + 1
		return self.pointer["Y"]*COL_COUNT + self.pointer["X"]

	@property
	def pointcell(self):
		return self.data[self.pointer['Y']][self.pointer['X']]

	@pointcell.setter
	def pointcell(self, value):
		self.data[self.pointer['Y']][self.pointer['X']] = value

	@property
	def move_direction(self):
		return {
			"down": {
				"X": 0, "Y": 1,
				"M": _("Bottom"),
			},
			"up": {
				"X": 0, "Y": -1,
				"M": _("Top"),
			},
			"left": {
				"X": -1, "Y": 0,
				"M": _("Left"),
			},
			"right": {
				"X": 1, "Y": 0,
				"M": _("Right"),
			},
		}

	def move(self, direction, mode="adjacent"):
		if mode == "adjacent":
			x_move = self.move_direction[direction]['X']
			y_move = self.move_direction[direction]['Y']
			if self.pointer['X'] + x_move >= self.col_count \
				or self.pointer['Y'] + y_move >= self.row_count \
				or self.pointer['X'] + x_move < 0 \
				or self.pointer['Y'] + y_move < 0:
				return self.move_direction[direction]['M']
			else:
				self.pointer['X'] = self.pointer['X'] + x_move
				self.pointer['Y'] = self.pointer['Y'] + y_move
		elif mode == "marginal":
			if direction == "down":
				self.pointer['Y'] = self.row_count-1
			elif direction == "up":
				self.pointer['Y'] = 0
			elif direction == "left":
				self.pointer['X'] = 0
			elif direction == "right":
				self.pointer['X'] = self.col_count-1

		return True

	def insert(self, mode):
		X = self.pointer['X']
		Y = self.pointer['Y']
		if mode == "down":
			self.data.insert(Y+1, [self.insert_default(" ") for i in range(self.col_count)])
			self.pointer['Y'] += 1
			return mode
		elif mode == "up":
			self.data.insert(Y, [self.insert_default(" ") for i in range(self.col_count)])
			return mode
		elif mode == "left":
			for row in self.data:
				row.insert(X, self.insert_default(" "))
			return mode
		elif mode == "right":
			for row in self.data:
				row.insert(X+1, self.insert_default(" "))
			self.pointer['X'] += 1
			return mode

	def delete(self, mode):
		if mode == "col":
			X = self.pointer["X"]
			if self.col_count > 1:
				for row in self.data:
					row.remove(row[X])
				if X >= self.col_count:
					self.pointer["X"] = self.col_count - 1
				return True
			else:
				return False
		elif mode == "row":
			Y = self.pointer["Y"]
			if self.row_count > 1:
				self.data.remove(self.data[Y])
				if Y >= self.row_count:
					self.pointer["Y"] = self.row_count - 1
				return True
			else:
				return False

	def load(self, path):
		self.data.clear()
		with open(path, 'r', encoding='utf-8') as src_file:
			src_csv = reader(src_file)
			rows = []
			for row in src_csv:
				rows.append(row)
			col_count = min([len(row) for r in rows])
			for row in rows:
				t = [
					self.insert_default(row[i]) for i in range(col_count)
				]
				self.data.append(t)

	def save(self, path):
		with open(path, 'w', encoding='utf-8', newline='') as dst_file:
			dst_csv = writer(dst_file)
			for row in self.data:
				dst_csv.writerow([r.value for r in row])


class Plane(TDBase):
	insert_default = lambda self, value: Char(value)

class Table(TDBase):
	insert_default = lambda self, value: Str(value)
