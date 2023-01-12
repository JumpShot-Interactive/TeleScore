"""
Developed By: JumpShot Team
Written by: riscyseven
"""

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal
from PyQt6 import uic

from component.element.clock import Clock
from fileio.fileout import TextOut
from gm_resources import resourcePath

class PenaltyInstance(QWidget):
    emitRemove = pyqtSignal(object, bool)

    def __init__(self, player: str, time: str, tFormat: str, fileName: str, index: int, parent=None):
        super().__init__(parent)
        path = resourcePath("src/component/penalty/penaltyinstance.ui") # replaced complicated path logic with resourcePath()
        uic.loadUi(path, self) # Load the .ui file
        self.fileName = fileName
        self.nameOut = TextOut(fileName + "-name-" + str(index), self)
        self.timeOut = TextOut(fileName + "-time-" + str(index), self)

        self.nameOut.outputFile(player)
        self.plyr_lineEdit.setText(player)
        self.player = player

        self.clock = Clock(self._done, False, self.time_lineEdit, self.timeOut, self)
        self.clock.setTimeFormat(tFormat)
        self.clock.setClockFromStr(time)
        self.index = index
        self.edit_pushButton.clicked.connect(self._editClicked)
        self.rem_pushButton.clicked.connect(self._remClicked)
        
    def changeIndex(self, index):
        self.index = index
        self.timeOut.setOutputFile(self.fileName + "-time-" + str(index))
        self.nameOut.setOutputFile(self.fileName + "-name-" + str(index))
        self.nameOut.outputFile(self.player)
        self.clock.addTime(0, 0)

    def isRunning(self) -> bool:
        return self.clock.isRunning()

    def start(self):
        if (self.edit_pushButton.text() == "Done"):
            self._editClicked()
        self.edit_pushButton.setEnabled(False)
        self.clock.startClock()

    def stop(self):
        self.edit_pushButton.setEnabled(True)
        self.clock.stopClock()

    def getIndex(self) -> int:
        return self.index

    def clear(self):
        self.timeOut.outputFile("")
        self.nameOut.outputFile("")

    def _done(self):
        self.emitRemove.emit(self, True)

    def _editClicked(self):
        if (self.edit_pushButton.text() == "Edit"):
            self.time_lineEdit.setEnabled(True)
            self.plyr_lineEdit.setEnabled(True)
            self.edit_pushButton.setText("Done")
        else:
            self.clock.setClockFromStr(self.time_lineEdit.text())
            self.player = self.plyr_lineEdit.text()
            self.nameOut.outputFile(self.player)
            self.time_lineEdit.setEnabled(False)
            self.plyr_lineEdit.setEnabled(False)
            self.edit_pushButton.setText("Edit")

    def _remClicked(self):
        self.emitRemove.emit(self, False)
        

        

