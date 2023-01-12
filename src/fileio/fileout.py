"""
Developed By: JumpShot Team
Written by: riscyseven
"""

from abc import abstractmethod
from PyQt6.QtCore import QFile, QByteArray
from PyQt6.QtGui import QPixmap

class FileOut:
    def __init__(self, fileName, type, parent=None):
        self.type = "." + type
        self.fileName = fileName
        self.fileIO = QFile(fileName + self.type, parent)
        
    def setOutputFile(self, fileAddr: str):
        self.fileIO.setFileName(fileAddr + self.type)
        self.fileName = fileAddr
        self.outputFile(None)

    def getOutputFile(self) -> str:
        return self.fileName

    @abstractmethod
    def outputFile(self, value):
        pass

class TextOut(FileOut):
    def __init__(self, fileName="", parent=None):
        super().__init__(fileName, "txt", parent)

    # Override
    def outputFile(self, value):
        if (value == None):
            value = ""
        if (self.fileIO.open(QFile.OpenModeFlag.WriteOnly)):
            self.fileIO.write(QByteArray(bytes(value, "utf-8")))
            self.fileIO.close()

class ImageOut(FileOut):
    def __init__(self, fileName="", parent=None):
        super().__init__(fileName, "png", parent)

    # Override
    def outputFile(self, value: QPixmap=None):
        if (value != None):
            value.save(self.fileName + self.type, "PNG")