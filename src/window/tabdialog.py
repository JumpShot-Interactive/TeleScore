"""
Developed By: JumpShot Team
Written by: riscyseven
"""

from PyQt6.QtWidgets import QDialog
from PyQt6 import uic
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

from gm_resources import resourcePath

class TabDialog(QDialog):
    def __init__(self, tab, callBack, parent=None):
        super().__init__(parent)
        uic.loadUi(resourcePath("src/window/ui/tabdialog.ui"), self) # Load the .ui file
        self.layout().addWidget(tab)
        self._tab = tab
        self.setWindowIcon(QIcon(resourcePath("src/resources/icon.ico")))
        self.setWindowFlag(Qt.WindowType.WindowMaximizeButtonHint, True)
        self.setWindowFlag(Qt.WindowType.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, True)
        self._callBack = callBack
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)


    def getTab(self):
        return self._tab


    def closeEvent(self, event):
        self._callBack(self)
        event.accept()
