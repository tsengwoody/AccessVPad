import os
import sys
PATH = os.path.dirname(os.path.abspath(__file__))
PYTHON_PATH = os.path.join(PATH, 'lib')
sys.path.insert(0, PYTHON_PATH)
from csv import reader, writer
from globalPlugins.AccessVPad.lib.xml.etree import ElementTree as ET

import api
import addonHandler
import controlTypes
import eventHandler
import globalPluginHandler
from keyboardHandler import KeyboardInputGesture
from NVDAObjects import NVDAObject
from NVDAObjects.IAccessible import Button, IAccessible, WindowRoot
from NVDAObjects.window import Window
import scriptHandler
from scriptHandler import script
import speech
import textInfos
import tones
import ui

import wx

from .graph import Tree, Graph, DirectedGraph, Node, Edge
from .TD import Plane, Table
from .textInfos import *
from .models import *
from .views import *

addonHandler.initTranslation()

def in_PadWindow(obj):
	result = False
	while obj:
		if isinstance(obj, BaseWindow):
			result = True
			break
		obj = obj.parent

	return result

class RootModel:
	def __init__(self):
		self.windows = []
		self._active = 0
		self.max = 0
		self.obj = None
		# self.add_plane_window()
		# self.add_table_window()
		# self.add_tree_window()
		# self.add_graph_window()

	@property
	def active(self):
		return self._active

	@active.setter
	def active(self, value):
		try:
			previous_type = self.active_window["type"]
		except:
			previous_type = None
		self._active = value
		current_type = self.active_window["type"]
		if not previous_type == current_type:
			self.setFocus()

	@property
	def active_window(self):
		try:
			window = self.windows[self.active]
		except IndexError:
			window = None
		return window

	def add_plane_window(self):
		self.max += 1
		self.windows.append({
			"name": "new {count}".format(count=self.max),
			"type": "plane",
			"path": None,
			"data": Plane(10, 10)
		})
		self.active = len(self.windows)-1

	def add_table_window(self):
		self.max += 1
		self.windows.append({
			"name": "new {count}".format(count=self.max),
			"type": "table",
			"path": None,
			"data": Table(10, 10)
		})
		self.active = len(self.windows)-1

	def add_tree_window(self):
		self.max += 1
		self.windows.append({
			"name": "new {count}".format(count=self.max),
			"type": "tree",
			"data": Tree(2),
			"path": None,
		})
		self.active = len(self.windows)-1

	def add_graph_window(self):
		self.max += 1
		self.windows.append({
			"name": "new {count}".format(count=self.max),
			"type": "graph",
			"data": DirectedGraph(ET=ET),
			"data": DirectedGraph(path=os.path.join(PATH, "graph.graphml"), ET=ET),
			"path": None,
		})
		self.active = len(self.windows)-1

	def switch_count_window(self, count):
		self.active = (self.active + count)%len(self.windows)

	def switch_certain_window(self, count):
		dst_active = count-1
		self.active = dst_active if dst_active < len(self.windows) else self.active

	def remove_window(self, index):
		self.windows = self.windows[0:index] + self.windows[index+1:]
		self.active = len(self.windows)-1 if self.active >= len(self.windows) else self.active

	def setFocus(self):
		# no over view
		if in_PadWindow(api.getFocusObject()):
			parent = self.obj.parent
		else:
			parent = api.getFocusObject()

		if self.active_window:
			if self.active_window["type"] == "plane":
				self.obj = PlaneWindow(parent=parent, root=self)
			elif self.active_window["type"] == "table":
				self.obj = TableWindow(parent=parent, root=self)
			elif self.active_window["type"] == "tree":
				self.obj = TreeWindow(parent=parent, root=self)
			elif self.active_window["type"] == "graph":
				self.obj = GraphWindow(parent=parent, root=self)
			wx.CallLater(100, self.obj.setFocus)

class BaseWindow(Window):
	def __init__(self, parent, root):
		self.parent = parent
		self.rootModel = root
		self.shift = {i: i.upper() for i in "abcdefghijklmnopqrstuvwxyz"}
		self.shift = {
			",": "<",
			".": ">",
			"/": "?",
			";": ":",
			"'": '"',
			"[": "{",
			"]": "}",
			"-": "_",
			"=": "+",
			"1": "!",
			"2": "@",
			"3": "#",
			"4": "$",
			"5": "%",
			"6": "^",
			"7": "&",
			"8": "*",
			"9": "(",
			"0": ")",
			**self.shift
		}
		self.name = ""
		self.data = None
		self.set(**self.rootModel.active_window)

		super().__init__(windowHandle=self.parent.windowHandle)

	def set(self, type, name, data, *args, **kwargs):
		self.name = name + " - {type}".format(type=type)
		self.data = data
		try:
			self.syncTextInfoPosition()
		except BaseException as e:
			pass

	def setFocus(self):
		eventHandler.executeEvent("gainFocus", self)

	@script(
		gestures=["kb:NVDA+t"]
	)
	def script_review_title(self, gesture):
		# ui.message(self.name)
		ui.message(self.rootModel.active_window["name"])

	@script(
		gestures=["kb:escape"]
	)
	def script_escape(self, gesture):
		eventHandler.executeEvent("gainFocus", self.parent)

	@script(
		gestures=[
			"kb:control+n", "kb:control+t",
		]
	)
	def script_add_window(self, gesture):
		def show(event):
			with PadAddDialog(parent=main_frame) as padAddDialog:
				if padAddDialog.ShowModal() == wx.ID_OK:
					new_type = padAddDialog.GetType()
					if new_type == "plane":
						self.rootModel.add_plane_window()
					elif new_type == "table":
						self.rootModel.add_table_window()
					elif new_type == "tree":
						self.rootModel.add_tree_window()
					elif new_type == "graph":
						self.rootModel.add_graph_window()
					self.set(**self.rootModel.active_window)
					ui.message(_("add window"))
					ui.message(self.rootModel.active_window["name"])
		wx.CallAfter(show, None)

	@script(
		gestures=[
			"kb:control+w",
		]
	)
	def script_remove_window(self, gesture):
		if len(self.rootModel.windows)-1 <= 0:
			ui.message(_("cannot remove window"))
		self.rootModel.remove_window(self.rootModel.active)
		self.set(**self.rootModel.active_window)
		ui.message(_("remove window"))
		ui.message(self.rootModel.active_window["name"])

	@script(
		gestures=[
			"kb:leftArrow", "kb:rightArrow",
			"kb:control+tab", "kb:control+shift+tab",
			"kb:control+pageUp", "kb:control+pageDown",
		]+["kb:control+{number}".format(number=i) for i in range(10)]
	)
	def script_switch_window(self, gesture):
		if gesture.mainKeyName == "tab":
			if "shift" in gesture.modifierNames:
				self.rootModel.switch_count_window(-1)
			else:
				self.rootModel.switch_count_window(1)
		elif gesture.mainKeyName in [str(i) for i in range(10)]:
			self.rootModel.switch_certain_window(int(gesture.mainKeyName))
		elif gesture.mainKeyName == "pageUp":
			self.rootModel.switch_count_window(-1)
		elif gesture.mainKeyName == "pageDown":
			self.rootModel.switch_count_window(1)

		ui.message(self.rootModel.active_window["name"] +" - " +_("{number} of {total}").format(number=self.rootModel.active+1, total=len(self.rootModel.windows)))
		self.set(**self.rootModel.active_window)

class TDBaseWindow(BaseWindow):
	def getScript(self, gesture):
		if not isinstance(api.getNavigatorObject(), self.__class__):
			api.setNavigatorObject(self)
		if isinstance(gesture, KeyboardInputGesture):
			if (
				(len(gesture.modifierNames) == 0 or (len(gesture.modifierNames) == 1 and "shift" in gesture.modifierNames)) \
				and (
					gesture.mainKeyName in set("abcdefghijklmnopqrstuvwxyz1234567890-=[];',./") \
					or gesture.mainKeyName in ["delete"]+["numLockNumpad{number}".format(number=i) for i in range(10)] \
					+["numpadDecimal", "numpadPlus", "numpadMinus", "numpadMultiply", "numpadDivide"]
				)
			):
				return self.script_insert
			elif (
				len(gesture.modifierNames) == 0 \
				and not gesture.mainKeyName in ["numpad{number}".format(number=i) for i in range(10)] \
				+ ["numLock", "escape", "leftArrow", "rightArrow", "upArrow", "downArrow", "applications", "enter"] \
				+ ["home", "end", "pageUp", "pageDown", "f2"]
			):
				return lambda s: ui.message(_("no action"))

		return super().getScript(gesture)

	@script(
		gestures=[
			"kb:applications",
		]
	)
	def script_menu(self, gesture):
		def show(event):
			main_frame.PopupMenu(PlaneMenu(self, self.rootModel))

			# no auto focus because action will popuped dialog
			# wx.CallLater(100, self.setFocus)

		wx.CallAfter(show, None)

	@script(
		gestures=[
			"kb:leftArrow", "kb:rightArrow",
			"kb:upArrow", "kb:downArrow",
			"kb:home", "kb:end",
			"kb:shift+home", "kb:shift+end",
		]
	)
	def script_arrow(self, gesture):
		if gesture.mainKeyName in ["upArrow", "downArrow", "leftArrow", "rightArrow"]:
			result = self.data.move(gesture.mainKeyName[:-5])
			if not result == True:
				ui.reviewMessage(result)
		elif gesture.mainKeyName in ["home", "end"]:
			if len(gesture.modifierNames) == 1 and "shift" in gesture.modifierNames:
				if gesture.mainKeyName == "home":
					self.data.move(direction="up", mode="marginal")
				elif gesture.mainKeyName == "end":
					self.data.move(direction="down", mode="marginal")
			else:
				if gesture.mainKeyName == "home":
					self.data.move(direction="left", mode="marginal")
				elif gesture.mainKeyName == "end":
					self.data.move(direction="right", mode="marginal")

		ui.message(self.data.pointcell.value)
		self.syncTextInfoPosition()

	@script(
		gestures=[
			"kb:alt+leftArrow", "kb:alt+rightArrow",
			"kb:alt+upArrow", "kb:alt+downArrow",
		]
	)
	def script_insert_cell(self, gesture):
		mode = self.data.insert(gesture.mainKeyName[:-5])
		if mode == "down":
			ui.message(_("insert new row at down"))
		elif mode == "up":
			ui.message(_("insert new row at up"))
		elif mode == "left":
			ui.message(_("insert new column at left"))
		elif mode == "right":
			ui.message(_("insert new column at right"))
		self.syncTextInfoPosition()

	@script(
		gestures=["kb:alt+delete"]
	)
	def script_delete_cell_row(self, gesture):
		if self.data.delete("row"):
			ui.message(_("delete row success"))
		else:
			ui.message(_("cannot delete row"))

		self.syncTextInfoPosition()

	@script(
		gestures=["kb:alt+shift+delete"]
	)
	def script_delete_cell_column(self, gesture):
		if self.data.delete("col"):
			ui.message(_("delete column success"))
		else:
			ui.message(_("cannot delete column"))

		self.syncTextInfoPosition()

	def script_insert(self, gesture):
		if gesture.mainKeyName == "delete":
			insert = " "
		elif gesture.mainKeyName.startswith("numLockNumpad"):
			insert = gesture.mainKeyName[-1]
		elif gesture.mainKeyName.startswith("numpad"):
			if gesture.mainKeyName == "numpadDecimal":
				insert = "."
			elif gesture.mainKeyName == "numpadPlus":
				insert = "+"
			elif gesture.mainKeyName == "numpadMinus":
				insert = "-"
			elif gesture.mainKeyName == "numpadMultiply":
				insert = "*"
			elif gesture.mainKeyName == "numpadDivide":
				insert = "/"
		elif len(gesture.modifierNames) == 1 and "shift" in gesture.modifierNames:
			insert = self.shift[gesture.mainKeyName]
		else:
			insert = gesture.mainKeyName

		self.data.pointcell.value = insert
		ui.message(insert)

	@script(
		gestures=["kb:NVDA+numpadDelete", "kb(laptop):NVDA+delete"]
	)
	def script_review_summary(self, gesture):
		repeats = scriptHandler.getLastScriptRepeatCount()
		if repeats == 0:
			ui.message(_("row {row} column {column}").format(row=self.data.pointer["Y"]+1, column=self.data.pointer["X"]+1))
		else:
			ui.message(_("{row} row {column} column").format(row=self.data.row_count, column=self.data.col_count))

	@script(
		gestures=['kb:f2']
	)
	def script_dialog_insert(self, gesture):
		def show(event):
			with InsertCellDialog(parent=main_frame, value=self.data.pointcell.value) as entryDialog:
				if entryDialog.ShowModal() == wx.ID_OK:
					self.data.pointcell.value = entryDialog.GetValue()
			wx.CallLater(100, self.setFocus)

		wx.CallAfter(show, None)

class PlaneWindow(TDBaseWindow):
	def makeTextInfo(self, position=textInfos.POSITION_FIRST):
		return PlaneWindowTextInfo(self, position)

	def syncTextInfoPosition(self):
		charInfo=api.getReviewPosition().obj.makeTextInfo(textInfos.POSITION_FIRST)
		charInfo.expand(textInfos.UNIT_CHARACTER)
		charInfo.collapse()
		res=charInfo.move(textInfos.UNIT_CHARACTER, self.data.linear_pos)
		api.setReviewPosition(charInfo)

	@script(
		gestures=['kb:control+o']
	)
	def script_dialog_open(self, gesture):
		def show(event):
			with wx.FileDialog(main_frame, message=_("Open file..."), wildcard="csv files (*.csv)|*.csv") as entryDialog:
				if entryDialog.ShowModal() != wx.ID_OK:
					return wx.CallLater(100, self.setFocus)
				src = entryDialog.GetPath()

			self.rootModel.add_plane_window()
			self.set(**self.rootModel.active_window)
			self.data.load(src)
			self.rootModel.active_window["name"] = os.path.basename(src).split(".")[0]
			self.set(**self.rootModel.active_window)
			wx.CallLater(100, self.setFocus)

		wx.CallAfter(show, None)

	@script(
		gestures=['kb:control+s']
	)
	def script_dialog_save(self, gesture):
		def show(event):
			if not self.rootModel.active_window["path"]:
				with wx.FileDialog(main_frame, message=_("Save file..."), wildcard="csv files (*.csv)|*.csv", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as entryDialog:
					if entryDialog.ShowModal() != wx.ID_OK:
						return wx.CallLater(100, self.setFocus)
					self.rootModel.active_window["path"] = dst = entryDialog.GetPath()
			else:
				dst = self.rootModel.active_window["path"]

			self.data.save(dst)
			self.rootModel.active_window["name"] = os.path.basename(dst).split(".")[0]
			self.set(**self.rootModel.active_window)
			wx.CallLater(100, self.setFocus)

		wx.CallAfter(show, None)

class TableWindow(TDBaseWindow):
	def makeTextInfo(self, position=textInfos.POSITION_FIRST):
		return TableWindowTextInfo(self, position)

	def syncTextInfoPosition(self):
		charInfo=api.getReviewPosition().obj.makeTextInfo(textInfos.POSITION_FIRST)
		charInfo.expand(textInfos.UNIT_CHARACTER)
		charInfo.collapse()
		api.setReviewPosition(charInfo)

	@script(
		gestures=['kb:control+o']
	)
	def script_dialog_open(self, gesture):
		def show(event):
			with wx.FileDialog(main_frame, message=_("Open file..."), wildcard="csv files (*.csv)|*.csv") as entryDialog:
				if entryDialog.ShowModal() != wx.ID_OK:
					return wx.CallLater(100, self.setFocus)
				src = entryDialog.GetPath()

			self.rootModel.add_table_window()
			self.set(**self.rootModel.active_window)
			self.data.load(src)
			self.rootModel.active_window["name"] = os.path.basename(src).split(".")[0]
			self.set(**self.rootModel.active_window)
			wx.CallLater(100, self.setFocus)

		wx.CallAfter(show, None)

	@script(
		gestures=['kb:control+s']
	)
	def script_dialog_save(self, gesture):
		def show(event):
			if not self.rootModel.active_window["path"]:
				with wx.FileDialog(main_frame, message=_("Save file..."), wildcard="csv files (*.csv)|*.csv", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as entryDialog:
					if entryDialog.ShowModal() != wx.ID_OK:
						return wx.CallLater(100, self.setFocus)
					self.rootModel.active_window["path"] = dst = entryDialog.GetPath()
			else:
				dst = self.rootModel.active_window["path"]

			self.data.save(dst)
			self.rootModel.active_window["name"] = os.path.basename(dst).split(".")[0]
			self.set(**self.rootModel.active_window)
			wx.CallLater(100, self.setFocus)

		wx.CallAfter(show, None)

		# gesture.send()

class TreeWindow(BaseWindow):
	def makeTextInfo(self, position=textInfos.POSITION_FIRST):
		return TreeWindowTextInfo(self, position)

	def syncTextInfoPosition(self):
		charInfo=api.getReviewPosition().obj.makeTextInfo(textInfos.POSITION_FIRST)
		charInfo.expand(textInfos.UNIT_CHARACTER)
		charInfo.collapse()
		api.setReviewPosition(charInfo)

	def getScript(self, gesture):
		if not isinstance(api.getNavigatorObject(), self.__class__):
			api.setNavigatorObject(self)
		return super().getScript(gesture)

	@script(
		gestures=[
			"kb:upArrow", "kb:shift+upArrow", "kb:enter", "kb:shift+enter",
		]
	)
	def script_node(self, gesture):
		if gesture.mainKeyName == "upArrow":
			result = True
		elif gesture.mainKeyName == "enter":
			if len(gesture.modifierNames) == 1 and "shift" in gesture.modifierNames:
				result = self.data.reverse_walk()
			else:
				result = self.data.forward_walk()

		if result:
			pointer = self.data.pointer
			ui.message(pointer.label)
		else:
			tones.beep(100, 100)

	@script(
		gestures=[
			"kb:leftArrow", "kb:rightArrow", "kb:downArrow",
			"kb:shift+leftArrow", "kb:shift+rightArrow", "kb:shift+downArrow",
		]
	)
	def script_edge(self, gesture):
		if gesture.mainKeyName == "downArrow":
			if len(gesture.modifierNames) == 1 and "shift" in gesture.modifierNames:
				pointer = self.data.point_in_edge
			else:
				pointer = self.data.point_out_edge
			result = True
		elif gesture.mainKeyName == "leftArrow":
			if len(gesture.modifierNames) == 1 and "shift" in gesture.modifierNames:
				result = self.data.previous_in()
				pointer = self.data.point_in_edge
			else:
				result = self.data.previous_out()
				pointer = self.data.point_out_edge
		elif gesture.mainKeyName == "rightArrow":
			if len(gesture.modifierNames) == 1 and "shift" in gesture.modifierNames:
				result = self.data.next_in()
				pointer = self.data.point_in_edge
			else:
				result = self.data.next_out()
				pointer = self.data.point_out_edge

		if not pointer:
			tones.beep(100, 100)
			return

		if not result:
			tones.beep(100, 100)

		if len(gesture.modifierNames) == 1 and "shift" in gesture.modifierNames:
			if not pointer.label == "":
				ui.message(_("{} by {}").format(pointer.source.label, pointer.label))
			else:
				ui.message("{}".format(pointer.source.label))
		else:
			if not pointer.label == "":
				ui.message(_("{} by {}").format(pointer.target.label, pointer.label))
			else:
				ui.message("{}".format(pointer.target.label))

class GraphWindow(BaseWindow):
	def makeTextInfo(self, position=textInfos.POSITION_FIRST):
		return GraphWindowTextInfo(self, position)

	def syncTextInfoPosition(self):
		charInfo=api.getReviewPosition().obj.makeTextInfo(textInfos.POSITION_FIRST)
		charInfo.expand(textInfos.UNIT_CHARACTER)
		charInfo.collapse()
		api.setReviewPosition(charInfo)

	def getScript(self, gesture):
		if not isinstance(api.getNavigatorObject(), self.__class__):
			api.setNavigatorObject(self)
		return super().getScript(gesture)

	@script(
		gestures=['kb:control+o']
	)
	def script_dialog_open(self, gesture):
		def show(event):
			with wx.FileDialog(main_frame, message=_("Open file..."), wildcard="GraphML files (*.graphml)|*.graphml") as entryDialog:
				if entryDialog.ShowModal() != wx.ID_OK:
					return wx.CallLater(100, self.setFocus)
				src = entryDialog.GetPath()

			self.rootModel.add_graph_window()
			self.set(**self.rootModel.active_window)
			self.data.load(src, ET)
			self.rootModel.active_window["name"] = os.path.basename(src).split(".")[0]
			self.set(**self.rootModel.active_window)
			wx.CallLater(100, self.setFocus)

		wx.CallAfter(show, None)

	@script(
		gestures=["kb:NVDA+numpadDelete", "kb(laptop):NVDA+delete"]
	)
	def script_review_summary(self, gesture):
		repeats = scriptHandler.getLastScriptRepeatCount()
		if repeats == 0:
			ui.message(_("{} edge in {} edge out".format(len(self.data.pointer.in_edges), len(self.data.pointer.out_edges))))
		else:
			ui.message(_("{} node {} edge".format(len(self.data.node_list), len(self.data.edge_list))))

	@script(
		gestures=["kb:n"]
	)
	def script_next_node(self, gesture):
		if not self.data.next_node():
			tones.beep(100, 100)
		pointer = self.data.pointer
		ui.message(pointer.label)

	@script(
		gestures=["kb:shift+n"]
	)
	def script_previous_node(self, gesture):
		if not self.data.previous_node():
			tones.beep(100, 100)
		pointer = self.data.pointer
		ui.message(pointer.label)

	@script(
		gestures=["kb:e"]
	)
	def script_next_edge(self, gesture):
		if not self.data.next_edge():
			tones.beep(100, 100)
		pointer = self.data.pointer
		if pointer:
			ui.message(pointer.label)

	@script(
		gestures=["kb:shift+e"]
	)
	def script_previous_edge(self, gesture):
		if not self.data.previous_edge():
			tones.beep(100, 100)
		pointer = self.data.pointer
		if pointer:
			ui.message(pointer.label)

	@script(
		gestures=[
			"kb:h"
		]
	)
	def script_forward_history(self, gesture):
		pointer = self.data.forward_history()
		if not pointer:
			tones.beep(100, 100)
			return
		if not pointer.label == "":
			ui.message("{} by {} to {}".format(pointer.source.label, pointer.label, pointer.target.label))
		else:
			ui.message("{} to {}".format(pointer.source.label, pointer.target.label))

	@script(
		gestures=[
			"kb:shift+h"
		]
	)
	def script_reverse_history(self, gesture):
		pointer = self.data.reverse_history()
		if not pointer:
			tones.beep(100, 100)
			return
		if not pointer.label == "":
			ui.message("{} by {} to {}".format(pointer.source.label, pointer.label, pointer.target.label))
		else:
			ui.message("{} to {}".format(pointer.source.label, pointer.target.label))

	@script(
		gestures=[
			"kb:upArrow", "kb:shift+upArrow", "kb:enter", "kb:shift+enter",
			"kb:z", "kb:c",
		]
	)
	def script_node(self, gesture):
		self.data.mode = "node"
		pointer = None
		if gesture.mainKeyName == "upArrow":
			pointer = self.data.pointer
			result = True
			ui.message(_("step{}").format(self.data.step))
		elif gesture.mainKeyName == "enter":
			if len(gesture.modifierNames) == 1 and "shift" in gesture.modifierNames:
				result = self.data.reverse_walk()
			else:
				result = self.data.forward_walk()
			pointer = self.data.pointer
			ui.message(_("step{}").format(self.data.step))
		elif gesture.mainKeyName == "z":
			if scriptHandler.getLastScriptRepeatCount() == 2:
				self.data.node_pointer = pointer = self.data.edge_pointer.source
			else:
				pointer = self.data.edge_pointer.source
			result = True
		elif gesture.mainKeyName == "c":
			if scriptHandler.getLastScriptRepeatCount() == 2:
				self.data.node_pointer = pointer = self.data.edge_pointer.target
			else:
				pointer = self.data.edge_pointer.target
			result = True

		if not result:
			tones.beep(100, 100)
		if pointer:
			ui.message(pointer.label)
		self.syncTextInfoPosition()

	@script(
		gestures=[
			"kb:leftArrow", "kb:rightArrow", "kb:downArrow",
			"kb:shift+leftArrow", "kb:shift+rightArrow", "kb:shift+downArrow",
			"kb:x",
		]
	)
	def script_edge(self, gesture):
		pointer = None
		if gesture.mainKeyName == "downArrow":
			if len(gesture.modifierNames) == 1 and "shift" in gesture.modifierNames:
				result = self.data.current_in()
				pointer = self.data.point_in_edge
			else:
				result = self.data.current_out()
				pointer = self.data.point_out_edge
		elif gesture.mainKeyName == "leftArrow":
			if len(gesture.modifierNames) == 1 and "shift" in gesture.modifierNames:
				result = self.data.previous_in()
				pointer = self.data.point_in_edge
			else:
				result = self.data.previous_out()
				pointer = self.data.point_out_edge
		elif gesture.mainKeyName == "rightArrow":
			if len(gesture.modifierNames) == 1 and "shift" in gesture.modifierNames:
				result = self.data.next_in()
				pointer = self.data.point_in_edge
			else:
				result = self.data.next_out()
				pointer = self.data.point_out_edge
		elif gesture.mainKeyName == "x":
			pointer = self.data.edge_pointer
			if not pointer:
				tones.beep(100, 100)
				return
			else:
				ui.message(pointer.label)
			return

		if not pointer:
			tones.beep(100, 100)
			return

		if not result:
			tones.beep(100, 100)

		if len(gesture.modifierNames) == 1 and "shift" in gesture.modifierNames:
			if not pointer.label == "":
				ui.message(_("{} by {}").format(pointer.source.label, pointer.label))
			else:
				ui.message("{}".format(pointer.source.label))
		else:
			if not pointer.label == "":
				ui.message(_("{} by {}").format(pointer.target.label, pointer.label))
			else:
				ui.message("{}".format(pointer.target.label))

	@script(
		gestures=['kb:f2']
	)
	def script_dialog_insert(self, gesture):
		def show(event):
			with wx.TextEntryDialog(parent=main_frame, message=_("enter node label"), value=self.data.node_pointer.label) as entryDialog:
				if entryDialog.ShowModal() == wx.ID_OK:
					self.data.node_pointer.label = entryDialog.GetValue()
			wx.CallLater(100, self.setFocus)

		wx.CallAfter(show, None)

	@script(
		gestures=[
			"kb:alt+n",
		]
	)
	def script_add_node(self, gesture):
		def show(event):
			with GraphAddNodeDialog(parent=main_frame) as dialog:
				if dialog.ShowModal() == wx.ID_OK:
					label = dialog.labelWidget.GetValue()
					self.data.add_node(label)
					ui.message(_("add node {}".format(label)))
		wx.CallAfter(show, None)

	@script(
		gestures=[
			"kb:alt+e",
		]
	)
	def script_add_edge(self, gesture):
		def show(event):
			with GraphAddEdgeDialog(parent=main_frame, nodes=self.data.node_list) as dialog:
				if dialog.ShowModal() == wx.ID_OK:
					source_index = dialog.sourceWidget.GetSelection()
					source = self.data.node_list[source_index]
					label = dialog.labelWidget.GetValue()
					target_index = dialog.targetWidget.GetSelection()
					target = self.data.node_list[target_index]
					self.data.add_edge(source=source.id, label=label, target=target.id)
					ui.message(_("add edge {}".format(label)))
		wx.CallAfter(show, None)

class AppWindowRoot(IAccessible):
	def event_focusEntered(self):
		parent = api.getFocusObject()
		if not hasattr(self, "obj"):
			self.obj = rootModel
		elif not self.obj:
			self.obj = rootModel
		self.obj.setFocus()

review_modes = [
	('object', _("Object review"), PlaneWindowTextInfo),
]


rootModel = RootModel()
main_frame = None

ADDON_SUMMARY = "AccessVPad"

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.windowClassName == "wxWindowNR" and obj.role == controlTypes.ROLE_WINDOW and obj.name == "AccessVPad":
			clsList.insert(0, AppWindowRoot)

	@script(
		gesture="kb:NVDA+alt+d",
		description=_("view AccessVPad content"),
		category=ADDON_SUMMARY,
	)
	def script_obj_interaction(self, gesture):
		if not in_PadWindow(api.getFocusObject()):
			global main_frame
			if not main_frame:
				main_frame = MainFrame(rootModel=rootModel)
			main_frame.Show()
			main_frame.Raise()
		else:
			ui.message(_("pad window is opened"))
