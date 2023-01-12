"""
Developed By: JumpShot Team
Written by: riscyseven
"""

from PyQt6.QtWidgets import QWidget, QFileDialog
from PyQt6 import uic
from gm_resources import resourcePath
from attr import PropWidgetType

class FileSelWidget(QWidget):
    def __init__(self, mode, callback, fileName="", parent=None):
        super().__init__(parent)
        path = resourcePath("src/editor/proptab/fileseldialog.ui") # replaced complicated path logic with resourcePath()
        uic.loadUi(path, self) # Load the .ui file
        self.lineEdit.setText(fileName)
        match mode:
            case PropWidgetType.FLOPEN:
                self.absPathButton.clicked.connect(self._openFile)
            case PropWidgetType.FLSAVE:
                self.absPathButton.clicked.connect(self._saveFile)
            case PropWidgetType.DRSAVE:
                self.absPathButton.clicked.connect(self._saveDir)

        self.callBack = callback
        self.lineEdit.textEdited.connect(self._textEdited)
        self.clrButton.clicked.connect(self._clrClicked)


    def _saveFile(self):
        fileName = QFileDialog.getSaveFileName(caption="Set File", directory="")
        if (fileName[0] != '' and fileName[0] != ''):
            fileName = fileName[0]
            if (".txt" in fileName):
                fileName = fileName.replace(".txt", "")
            self.lineEdit.setText(fileName)
            self._textEdited()


    def _openFile(self):
        fileName = QFileDialog.getOpenFileName(caption="Open File", directory="")
        if (fileName[0] != '' and fileName[0] != ''):
            self.lineEdit.setText(fileName[0])
            self._textEdited()


    def _saveDir(self):
        dirName = QFileDialog.getExistingDirectory(caption="Set Folder", directory="")
        if (dirName != ''):
            self.lineEdit.setText(dirName)
            self._textEdited()


    def _textEdited(self, text=""):
        self.callBack(self.lineEdit.text())


    def _clrClicked(self):
        self.lineEdit.clear()
        self._textEdited()