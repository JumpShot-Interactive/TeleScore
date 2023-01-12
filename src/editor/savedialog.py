"""
Developed By: JumpShot Team
Written by: riscyseven
"""

from PyQt6.QtWidgets import QDialog
from PyQt6 import uic

from gm_resources import resourcePath

class SaveDialog(QDialog):
    CANCEL = 0
    REJECT = 1

    def __init__(self, parent=None):
        super().__init__(parent)
        path = resourcePath("src/editor/savedialog.ui") # replaced complicated path logic with resourcePath()
        uic.loadUi(path, self) # Load the .ui file
        self.buttonBox.clicked.connect(self._buttonClicked)
        self._code = 0


    def _buttonClicked(self, button):
        
        if (button == self.buttonBox.button(self.buttonBox.StandardButton.Save)):
            self.accept()
        elif (button == self.buttonBox.button(self.buttonBox.StandardButton.Discard)):
            self._code = self.REJECT
            self.reject()
        else:
            self._code = self.CANCEL
            self.reject()


    def getCode(self) -> int:
        return self._code