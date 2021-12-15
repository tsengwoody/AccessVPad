import addonHandler
import globalVars
import wx

from gui import guiHelper

addonHandler.initTranslation()

def add_pad(parent):
	with PadAddDialog(parent=parent) as padAddDialog:
		if padAddDialog.ShowModal() == wx.ID_OK:
			new_type = padAddDialog.GetType()
			if new_type == "plane":
				globalVars.rootModel.add_plane_window()
			elif new_type == "table":
				globalVars.rootModel.add_table_window()
			elif new_type == "tree":
				globalVars.rootModel.add_tree_window()
			elif new_type == "graph":
				globalVars.rootModel.add_graph_window()

class GenericFrame(wx.Frame):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.buttons = []

		self.CreateStatusBar() # A StatusBar in the bottom of the window
		self.createMenuBar()

		self.panel = wx.Panel(self, -1)
		self.createButtonBar(self.panel)

		mainSizer=wx.BoxSizer(wx.HORIZONTAL)
		for button in self.buttons:
			mainSizer.Add(button)

		self.panel.SetSizer(mainSizer)
		mainSizer.Fit(self)

	def menuData(self):
		return [
		]

	def createMenuBar(self):
		self.menuBar = wx.MenuBar()
		for eachMenuData in self.menuData():
			menuLabel = eachMenuData[0]
			menuItems = eachMenuData[1]
			self.menuBar.Append(self.createMenu(menuItems), menuLabel)

		self.SetMenuBar(self.menuBar)

	def createMenu(self, menuData):
		menu = wx.Menu()
		for eachItem in menuData:
			if len(eachItem) == 2:
				label = eachItem[0]
				subMenu = self.createMenu(eachItem[1])
				menu.AppendMenu(wx.NewId(), label, subMenu)

			else:
				self.createMenuItem(menu, *eachItem)
		return menu

	def createMenuItem(self, menu, label, status, handler, kind=wx.ITEM_NORMAL):
		if not label:
			menu.AppendSeparator()
			return
		menuItem = menu.Append(-1, label, status, kind)
		self.Bind(wx.EVT_MENU, handler, menuItem)

	def buttonData(self):
		return [
		]

	def createButtonBar(self, panel, yPos = 0):
		xPos = 0
		for eachLabel, eachHandler in self.buttonData():
			pos = (xPos, yPos)
			button = self.buildOneButton(panel, eachLabel,eachHandler, pos)
			self.buttons.append(button)
			xPos += button.GetSize().width

	def buildOneButton(self, parent, label, handler, pos=(0,0)):
		button = wx.Button(parent, -1, label, pos)
		self.Bind(wx.EVT_BUTTON, handler, button)
		return button

class MainFrame(GenericFrame):
	def __init__(self):
		title = _("AccessVPad")
		super().__init__(wx.GetApp().TopWindow, title=title)
		self.Bind(wx.EVT_CLOSE, self.OnClose)

	def OnClose(self, event):
		self.Destroy()
		globalVars.mainFrame = None

	def menuData(self):
		return [
			(_("&Menu"), (
				(_("&Exit"),_("Terminate the program"), self.OnClose),
			))
		]

	def buttonData(self):
		return (
			(_("pad"), self.OnPad),
		)

	def OnExit(self, event):
		self.OnClose()

	def OnPad(self, event):
		if globalVars.rootModel.active_window:
			globalVars.rootModel.setFocus()
		else:
			wx.CallAfter(add_pad, self)

class PadAddDialog(wx.Dialog):
	TYPE_CHOICES = {
		0: "plane",
		1: "table",
		# 2: "tree",
		# 2: "graph",
	}

	def __init__(self, parent):
		super().__init__(parent, title=_("New pad"))

		mainSizer = wx.BoxSizer(wx.VERTICAL)

		sHelper = guiHelper.BoxSizerHelper(self, orientation=wx.VERTICAL)
		typeChoices = [i for i in self.TYPE_CHOICES.values()]
		typeLabelText = _("&Type:")
		self.typeWidget = sHelper.addLabeledControl(typeLabelText, wx.Choice, choices=typeChoices)
		sHelper.addDialogDismissButtons(self.CreateButtonSizer(wx.OK | wx.CANCEL))

		# bHelper = guiHelper.ButtonHelper(orientation=wx.HORIZONTAL)
		# OkButton = bHelper.addButton(self, label=_("OK"), id=wx.ID_OK)
		# CancelButton = bHelper.addButton(self, label=_("Cancel"), id=wx.ID_CANCEL)

		# self.Bind(wx.EVT_BUTTON, self.onOk, id=wx.ID_OK)
		# self.Bind(wx.EVT_BUTTON, self.onCancel, id=wx.ID_CANCEL)
		self.Bind(wx.EVT_CHAR_HOOK, self._enterActivatesOk_ctrlSActivatesApply)

		mainSizer.Add(sHelper.sizer, border=guiHelper.BORDER_FOR_DIALOGS, flag=wx.ALL)
		# mainSizer.Add(bHelper.sizer, border=guiHelper.BORDER_FOR_DIALOGS, flag=wx.ALL)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)

		self.typeWidget.SetSelection(0)

	def GetType(self):
		return self.TYPE_CHOICES[self.typeWidget.GetSelection()]

	def _enterActivatesOk_ctrlSActivatesApply(self, evt):
		if evt.KeyCode in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER):
			self.ProcessEvent(wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, wx.ID_OK))
		else:
			evt.Skip()


class GraphAddNodeDialog(wx.Dialog):
	def __init__(self, parent):
		super().__init__(parent, title=_("New node"))

		mainSizer = wx.BoxSizer(wx.VERTICAL)

		sHelper = guiHelper.BoxSizerHelper(self, orientation=wx.VERTICAL)
		self.labelWidget = sHelper.addLabeledControl(_("&Label:"), wx.TextCtrl)
		sHelper.addDialogDismissButtons(self.CreateButtonSizer(wx.OK | wx.CANCEL))

		self.Bind(wx.EVT_CHAR_HOOK, self._enterActivatesOk_ctrlSActivatesApply)

		mainSizer.Add(sHelper.sizer, border=guiHelper.BORDER_FOR_DIALOGS, flag=wx.ALL)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)

	def _enterActivatesOk_ctrlSActivatesApply(self, evt):
		if evt.KeyCode in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER):
			self.ProcessEvent(wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, wx.ID_OK))
		else:
			evt.Skip()


class GraphAddEdgeDialog(wx.Dialog):
	def __init__(self, parent, nodes):
		super().__init__(parent, title=_("New edge"))

		self.nodes = nodes

		mainSizer = wx.BoxSizer(wx.VERTICAL)
		sHelper = guiHelper.BoxSizerHelper(self, orientation=wx.VERTICAL)

		self.labelWidget = sHelper.addLabeledControl(_("&Label:"), wx.TextCtrl)

		sourceChoices = [i.label for i in self.nodes]
		sourceLabelText = _("&Source:")
		self.sourceWidget = sHelper.addLabeledControl(sourceLabelText, wx.Choice, choices=sourceChoices)

		targetChoices = [i.label for i in self.nodes]
		targetLabelText = _("&Target:")
		self.targetWidget = sHelper.addLabeledControl(targetLabelText, wx.Choice, choices=targetChoices)

		sHelper.addDialogDismissButtons(self.CreateButtonSizer(wx.OK | wx.CANCEL))
		self.Bind(wx.EVT_CHAR_HOOK, self._enterActivatesOk_ctrlSActivatesApply)

		mainSizer.Add(sHelper.sizer, border=guiHelper.BORDER_FOR_DIALOGS, flag=wx.ALL)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)

	def _enterActivatesOk_ctrlSActivatesApply(self, evt):
		if evt.KeyCode in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER):
			self.ProcessEvent(wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, wx.ID_OK))
		else:
			evt.Skip()


class InsertCellDialog(wx.TextEntryDialog):
	def __init__(self, parent, message=_("enter cell value"), value=""):
		super().__init__(parent=parent,message=message, value=value)

class TDBaseMenu(wx.Menu):
	def __init__(self, parent, root):
		self.parent = parent
		self.rootModel = root
		self.data = None
		self.set(**self.rootModel.active_window)

		super().__init__()

		for item in self.menuData:
			if 'menu' in item:
				label = item['label']
				subMenu = self.createMenu(item['menu'])
				self.AppendMenu(wx.ID_ANY, label, subMenu)
			else:
				self.createMenuItem(self, **item)

	@property
	def menuData(self):
		return [
			{
				'id': 'add',
				'label': _('&Add'),
				'menu': [
					{
						'id': 'up-row',
						'label': _('&Up Row'),
						'action': self.insert_cell_up_row,
					},
					{
						'id': 'down-row',
						'label': _('&Down Row'),
						'action': self.insert_cell_down_row,
					},
					{
						'id': 'left-column',
						'label': _('&Left Column'),
						'action': self.insert_cell_left_column,
					},
					{
						'id': 'right-column',
						'label': _('&Right Column'),
						'action': self.insert_cell_right_column,
					},
				],
			},
			{
				'id': 'edit',
				'label': _('&Edit'),
				'action': self.dialog_insert,
			},
			{
				'id': 'delete',
				'label': _('&Delete'),
				'menu': [
					{
						'id': 'delete-row',
						'label': _('&Row'),
						'action': self.delete_row,
					},
					{
						'id': 'delete-column',
						'label': _('&Column'),
						'action': self.delete_column,
					},
				],
			},
		]

	def createMenu(self, menuData):
		menu = wx.Menu()
		for item in menuData:
			if 'menu' in item:
				label = item['label']
				subMenu = self.createMenu(item['menu'])
				menu.AppendMenu(wx.ID_ANY, label, subMenu)
			else:
				self.createMenuItem(menu, **item)
		return menu

	def createMenuItem(self, menu, id, label, action):
		menuItem = menu.Append(wx.ID_ANY, label)
		self.Bind(wx.EVT_MENU, action, menuItem)

	def set(self, data, *args, **kwargs):
		self.data = data

	def onNoAction(self, event):
		pass

	def insert_cell_up_row(self, event):
		self.data.insert('up')
		wx.CallLater(100, ui.message, (_("insert new row at up")))

	def insert_cell_down_row(self, event):
		self.data.insert('down')
		wx.CallLater(100, ui.message, (_("insert new row at down")))

	def insert_cell_left_column(self, event):
		self.data.insert('left')
		wx.CallLater(100, ui.message, (_("insert new column at left")))

	def insert_cell_right_column(self, event):
		self.data.insert('right')
		wx.CallLater(100, ui.message, (_("insert new column at right")))

	def dialog_insert(self, event):
		def show(event):
			with InsertCellDialog(parent=globalVars.mainFrame, value=self.data.pointcell.value) as entryDialog:
				if entryDialog.ShowModal() == wx.ID_OK:
					self.data.pointcell.value = entryDialog.GetValue()

		wx.CallAfter(show, None)

	def delete_row(self, event):
		if self.data.delete("row"):
			wx.CallLater(100, ui.message, (_("delete row success")))
		else:
			wx.CallLater(100, ui.message, (_("cannot delete row")))

	def delete_column(self, event):
		if self.data.delete("col"):
			wx.CallLater(100, ui.message, (_("delete column success")))
		else:
			wx.CallLater(100, ui.message, (_("cannot delete column")))

class PlaneMenu(TDBaseMenu):
	pass

class TableMenu(TDBaseMenu):
	pass
