"""
Developed By: JumpShot Team
Written by: riscyseven
"""

from PyQt6.QtWidgets import QGridLayout
from PyQt6.QtCore import pyqtSignal, QSize, Qt
from PyQt6.QtGui import QResizeEvent, QMouseEvent

from abstract.abstractcomp import AbstractComp
from layout.ctrllayout import CtrlLayout
from attr import PropInstType, PropWidgetType, CompType

class TabComp(AbstractComp):
    attrChanged = pyqtSignal()
    LOClicked = pyqtSignal(object)

    loProperty = {
        "Width": {
            PropInstType.TYPE: PropWidgetType.NUMEDIT,
            PropInstType.VALUE: 800,
        },
        "Height": {
            PropInstType.TYPE: PropWidgetType.NUMEDIT,
            PropInstType.VALUE: 600
        },
        "Background Image": {
            PropInstType.TYPE: PropWidgetType.FLOPEN,
            PropInstType.VALUE: ""
        },
        "Background Color": {
            PropInstType.TYPE: PropWidgetType.COLORPICK,
            PropInstType.VALUE: "#000000"
        },
        "Maintain Aspect Ratio": {
            PropInstType.TYPE: PropWidgetType.CHECKBOX,
            PropInstType.VALUE: True
        },
        "Pop Out On Start": {
            PropInstType.TYPE: PropWidgetType.CHECKBOX,
            PropInstType.VALUE: False
        }
    }


    def __init__(self, project, objectName, remCallBack=None, dropCallBack=None, parent=None):
        super().__init__(project, objectName, CompType.LAYOUT, parent)
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.ctrl = CtrlLayout(project, QSize(800, 600), remCallBack, dropCallBack, self)
        self.layout.addWidget(self.ctrl, 0, Qt.AlignmentFlag.AlignCenter)
        self.ctrl.setStyleSheet("background-color: #3E5768;")
        self.aspectRatio = True

        self._firstTimeProp()


    def calcAspectRatioFit(self, projSize: QSize, size: QSize) -> QSize:
        """
        Calculates the size of the projection screen
        to fit the projection size

        :param projSize: QSize, the size of the projection
        :param size: QSize, the size of the screen
        :return: QSize, the size of the projection screen
        """
        ratio = min(size.width() / projSize.width(), size.height() / projSize.height())
        return QSize(round(projSize.width() * ratio), round(projSize.height() * ratio))


    def getLayout(self):
        return self.ctrl


    def resizeEvent(self, a0: QResizeEvent):
        newSize = a0.size()
        if (self.aspectRatio):
            newSize = self.calcAspectRatioFit(self.ctrl.getProjSize(), a0.size())
            self.ctrl.setMaximumSize(newSize)
        self.ctrl.layoutResized(newSize)


    # Override
    def getName(self) -> str:
        """
        Return the type of the component in str
        :param: none
        :return str: str that describes the component type
        """
        pass


    # Override
    def _firstTimeProp(self):
        """
        When the component is initialized, this is called to make
        sure the subclasses insert correct _properties. This method will be
        called automatially by the this base class.

        :param: none
        :return: none
        """
        self._properties.appendPropHead("Layout Properties", self.loProperty)


    # Override
    def _derPropRequested(self):
        """
        Called when the user modifies any attributes inside the property tab
        :param: none
        :return: none
        """
        self._properties["Width"] = self.ctrl.getProjSize().width()
        self._properties["Height"] = self.ctrl.getProjSize().height()
        self._properties["Background Color"] = self.ctrl.getBackgroundColor()
        self._properties["Maintain Aspect Ratio"] = self.aspectRatio


    # Override
    def _derPropChanged(self):
        """
        Reload attributes 
        """
        size = QSize(self._properties["Width"], self._properties["Height"])

        if (size.width() < 4000 and size.height() < 4000):
            if size != self.ctrl.getProjSize() and (size.width() > 0 and size.height() > 0):
                self.ctrl.setSize(self.ctrl.getProjSize())
                self.resizeEvent(QResizeEvent(self.ctrl.getProjSize(), self.ctrl.getProjSize()))
                self.ctrl.setSize(size)
                self.resizeEvent(QResizeEvent(self.size(), self.size()))

            if (self.aspectRatio != self._properties["Maintain Aspect Ratio"]):
                self.aspectRatio = self._properties["Maintain Aspect Ratio"]
                if (not self._properties["Maintain Aspect Ratio"]):
                    self.ctrl.setMaximumSize(16777215, 16777215)
                self.resizeEvent(QResizeEvent(self.size(), self.size()))

        if (len(self._properties["Background Image"]) > 0):
            self.ctrl.setBackgroundIMG(self._properties["Background Image"])
        else:
            self.ctrl.setBackgroundIMG(None)
        self.ctrl.setBackgroundColor(self._properties["Background Color"])
        

    def mousePressEvent(self, evt: QMouseEvent):
        self.LOClicked.emit(self)