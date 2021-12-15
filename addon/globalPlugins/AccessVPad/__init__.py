import os
import sys
PATH = os.path.dirname(__file__)
PYTHON_PATH = os.path.join(PATH, 'python')
sys.path.insert(0, PYTHON_PATH)
PACKAGE_PATH = os.path.join(PATH, 'package')
sys.path.insert(0, PACKAGE_PATH)
sys.path.insert(0, PATH)

import addonHandler
import api
import config
import controlTypes
import globalPluginHandler
import globalVars
import gui
from NVDAObjects.IAccessible import Button, IAccessible, WindowRoot
from scriptHandler import script
import ui
import wx

from .dialogs import AVPSettingsDialog
from .RootModel import RootModel, in_PadWindow
from .views import MainFrame, add_pad

addonHandler.initTranslation()

ADDON_SUMMARY = "AccessVPad"

config.conf.spec["AccessVPad"] = {
	"settings": {
		"show_main_frame": "boolean(default=false)",
		"border": "boolean(default=true)",
		"color": "string(default=#00e64d)",
	},
}
config.conf["AccessVPad"]["settings"]["show_main_frame"] = True


globalVars.rootModel = RootModel()
globalVars.mainFrame = MainFrame()

class AppWindowRoot(IAccessible):
	def event_focusEntered(self):
		globalVars.rootModel.setFocus()


import threading
from server.application import Shorty
from werkzeug.serving import run_simple

class RunServer(threading.Thread):
	def run(self):
		running = False
		host = '0.0.0.0'
		port = 8000
		while not running:
			try:
				globalVars.port = port
				run_simple(
					host,
					port,
					Shorty(),
					use_reloader=False,
					use_debugger=False,
				)
				running = True
			except OSError:
				port += 1

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.create_menu()
		RunServer().start()

	def terminate(self):
		try:
			self.toolsMenu.Remove(self.AccessVPad_item)
		except (AttributeError, RuntimeError):
			pass

	def create_menu(self):
		self.toolsMenu = gui.mainFrame.sysTrayIcon.toolsMenu
		self.menu = wx.Menu()

		self.pad = self.menu.Append(
			wx.ID_ANY,
			_("&Pad...")
		)
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onPad, self.pad)

		self.browser = self.menu.Append(
			wx.ID_ANY,
			_("&Browser...")
		)
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onBrowser, self.browser)

		self.settings = self.menu.Append(
			wx.ID_ANY,
			_("&Settings...")
		)
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onSettings, self.settings)

		self.AccessVPad_item = self.toolsMenu.AppendSubMenu(self.menu, _("AccessVPad"), _("AccessVPad"))

	def onPad(self, evt):
		self.openPad(show_main_frame=True)

	def onBrowser(self, evt):
		os.startfile('http://localhost:{port}/app/'.format(port=globalVars.port))

	def onSettings(self, evt):
		gui.mainFrame._popupSettingsDialog(AVPSettingsDialog, config.conf["AccessVPad"])

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.windowClassName == "wxWindowNR" and obj.role == controlTypes.ROLE_WINDOW and obj.name == "AccessVPad":
			clsList.insert(0, AppWindowRoot)

	@script(
		gesture="kb:NVDA+alt+d",
		description=_("view AccessVPad content"),
		category=ADDON_SUMMARY,
	)
	def script_obj_interaction(self, gesture):
		self.openPad(show_main_frame=config.conf["AccessVPad"]["settings"]["show_main_frame"])

	def openPad(self, show_main_frame):
		if not in_PadWindow(api.getFocusObject()):
			if show_main_frame:
				if not globalVars.mainFrame:
					globalVars.mainFrame = MainFrame()
				globalVars.mainFrame.Show()
				globalVars.mainFrame.Raise()
			else:
				if globalVars.rootModel.active_window:
					globalVars.rootModel.setFocus()
				else:
					if not globalVars.mainFrame:
						globalVars.mainFrame = MainFrame()
					globalVars.mainFrame.Show()
					globalVars.mainFrame.Raise()
		else:
			ui.message(_("pad window is opened"))
