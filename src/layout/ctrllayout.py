"""
Developed By: JumpShot Team
Written by: riscyseven
"""

# This Python file uses the following encoding: utf-8
from PyQt6.QtCore import QSize, pyqtSignal
from PyQt6.QtWidgets import QFrame, QBoxLayout

from abstract.layoutcomp import LayoutComp

from PyQt6.QtGui import QPainter, QPixmap, QPaintEvent

from layout.abstract_layout.freelayout import FreeLayout


class CtrlLayout(QFrame):
    """
    This class is the widget that wraps the freelayout class.
    """
    actiUpdate = pyqtSignal()

    def __init__(self, project=None, projSize=QSize(800, 600), remCallBack=None, dropCallBack=None, parent=None):
        super().__init__(parent)
        self._actualLayout = FreeLayout(projSize)
        self._remCallBack = remCallBack
        self._dropCallBack = dropCallBack
        self._backIMG = None
        self._projSize = None
        self._project = project

        self.setLayout(QBoxLayout(QBoxLayout.Direction.TopToBottom))
        self.setSize(projSize)
        self.setAcceptDrops(True)


    def setRemoveCallBack(self, callback):
        self._remCallBack = callback

    
    def setDropCallBack(self, callback):
        self._dropCallBack = callback


    def setSize(self, size: QSize):
        '''if (self._projSize != size):
            for comp in self._actualLayout.getLOWidgets():
                comp.initRatio(size, size)'''

        self._projSize = size


    def defaultSize(self):
        return self._projSize


    def layoutResized(self, size: QSize):
        """
        Anytime the control layout is resized, 
        this is called.

        :param event: QResizeEvent information 
        :return: none
        """
        '''for comp in self._actualLayout.getLOWidgets():
            comp.parentResized(size)'''

    def addComponent(self, component: LayoutComp):
        """
        Method that adds component to the layout.

        :param component: AbstractComp, a component to add
        :return: none
        """
        component.initRatio(self._projSize, self.size())
        self._actualLayout.addWidget(component)
        if (self._project != None):
            self._project.addComp(component.objectName(), component)
        self.actiUpdate.emit()


    def removeComponent(self, comp: LayoutComp) -> None:
        comp.getConnection().removeAllConnection()

        if (self._project != None):
            self._project.removeComp(comp)
        self._actualLayout.removeWidget(comp)
        if (self._remCallBack != None):
            self._remCallBack(comp)
        comp.setParent(None)
        comp.deleteLater()
        comp = None
        self.actiUpdate.emit()


    def dragEnterEvent(self, evt) -> None:
        """
        Method is called when anything dragged is entered.

        :param evt: event
        :return: none
        """
        if (evt.mimeData().hasFormat("application/x-comp")):
            evt.setAccepted(True)
            evt.acceptProposedAction()
            evt.accept()


    def count(self) -> int:
        return self._actualLayout.count()


    def dropEvent(self, evt):
        self._dropCallBack(evt, self)


    def getProjSize(self) -> QSize:
        return self._projSize


    def getCurrSize(self) -> QSize:
        return self.size()


    def setBackgroundColor(self, color: str):
        self.setStyleSheet(f"background-color:{color};")

    
    def getBackgroundColor(self) -> str:
        return self.styleSheet().split(":")[1].split(";")[0].strip()
    

    def setBackgroundIMG(self, img: str):
        if (img == None):
            self._backIMG = None
            return
        self._backIMG = img


    def paintEvent(self, evt: QPaintEvent):
        if (self._backIMG != None):
            img = QPixmap(self._backIMG)
            painter = QPainter(self)
            img = img.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            painter.drawPixmap(0, 0, img)
            painter.end()

    
    def getLOComp(self) -> list:
        #return self._actualLayout.getLOWidgets()
        return []

    
    def moveUp(self, comp: LayoutComp):
        self._actualLayout.moveUp(comp)
        self.actiUpdate.emit()


    def moveDown(self, comp: LayoutComp):
        self._actualLayout.moveDown(comp)
        self.actiUpdate.emit()
