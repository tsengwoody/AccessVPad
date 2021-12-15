from collections import OrderedDict
import os
import shutil
import wx

import addonHandler
import config
from gui import guiHelper
from gui.settingsDialogs import SettingsDialog
from logHandler import log
import tones

addonHandler.initTranslation()

class AVPSettingsDialog(SettingsDialog):
	# Translators: Title of the Access8MathDialog.
	title = _("Settings")
	settings = OrderedDict({
		# "show_main_frame": {
			# "label": _("Show AccessVPad window when entering interactive window")
		# },
		"border": {
			"label": _("Show border of the cell")
		},
		"color": {
			"label": _("Hightlight color of the cell pointed to by cursor:"),
			"options": {
				"#ff8566": _("red"),
				"#ffe680": _("yallow"),
				"#00e64d": _("green"),
				"#80b3ff": _("blue"),
				"#cc99ff": _("purple"),
			}
		},
	})

	def __init__(self, parent, config):
		self.config = config
		super().__init__(parent)

	def makeSettings(self, settingsSizer):
		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		for k, v in self.settings.items():
			if "options" in v:
				attr = k + "Selection"
				options = v["options"]
				widget = sHelper.addLabeledControl(v["label"], wx.Choice, choices=list(options.values()))
				setattr(self, attr, widget)
				try:
					index = list(v["options"].keys()).index(str(self.config["settings"][k]))
				except:
					index = 0
					tones.beep(100, 100)
				widget.Selection = index
			else:
				setattr(self, k + "CheckBox", sHelper.addItem(wx.CheckBox(self, label=v["label"])))
				value = self.config["settings"][k]
				getattr(self, k + "CheckBox").SetValue(value)

	def postInit(self):
		self.colorSelection.SetFocus()

	def onOk(self, evt):
		try:
			for k, v in self.settings.items():
				if "options" in v:
					attr = k + "Selection"
					widget = getattr(self, attr)
					self.config["settings"][k] = list(v["options"].keys())[widget.GetSelection()]
				else:
					self.config["settings"][k] = getattr(self, k + "CheckBox").IsChecked()
		except:
			for k, v in self.Selection_settings.items():
				if "options" in v:
					self.config["settings"][k] = list(v["options"].keys())[0]
				else:
					self.config["settings"][k] = True
			tones.beep(100, 100)

		return super().onOk(evt)
