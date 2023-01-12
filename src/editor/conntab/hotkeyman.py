"""
Developed By: JumpShot Team
Written by: riscyseven
"""

from PyQt6.QtWidgets import QWidget
from PyQt6 import uic
from PyQt6.QtGui import QKeySequence

from gm_resources import resourcePath

class HotkeyMan(QWidget):
    def __init__(self, data, callBack, parent=None):
        super().__init__(parent)
        path = resourcePath("src/editor/conntab/hotkeyman.ui")
        uic.loadUi(path, self) # Load the .ui file

        self.callBack = callBack
        self.keySequenceEdit.setKeySequence(QKeySequence(data))
        self.submit_pushButton.clicked.connect(self._editingFinished)
        self.clear_pushButton.clicked.connect(self._clearButtonClicked)

    def _editingFinished(self):
        value = self.keySequenceEdit.keySequence()[0]
        seq = QKeySequence(value)
        self.keySequenceEdit.setKeySequence(seq)
        self.callBack(seq.toString())

    def _clearButtonClicked(self):
        self.keySequenceEdit.clear()
        self.callBack("")


        

            




    
