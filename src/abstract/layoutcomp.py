"""
Developed by: JumpShot Team
Written by: riscyseven
"""

from PyQt6.QtWidgets import QMenu
from PyQt6 import uic
from PyQt6.QtCore import QPoint, Qt, QEvent, QObject, pyqtSignal, QSize
from PyQt6.QtGui import QMouseEvent, QContextMenuEvent, QAction

from attr import PropWidgetType, PropInstType
from gm_resources import resourcePath
from component.connection import Connection
from abstract.abstractcomp import AbstractComp

from abc import abstractmethod

class LayoutComp(AbstractComp):
    """
    Abstract class for components. All component classes should inherit this class

    Contains implmentation requirements for a component, also contains functions that
    are required for the editor
    """

    geoProperty = {
        "X": {
            PropInstType.TYPE: PropWidgetType.NUMEDIT,
            PropInstType.VALUE: 1
        },
        "Y": {
            PropInstType.TYPE: PropWidgetType.NUMEDIT,
            PropInstType.VALUE: 1
        },
        "Width": {
            PropInstType.TYPE: PropWidgetType.NUMEDIT,
            PropInstType.VALUE: 0
        },
        "Height": {
            PropInstType.TYPE: PropWidgetType.NUMEDIT,
            PropInstType.VALUE: 0
        }
    }

    compClicked = pyqtSignal(object)
    attrChanged = pyqtSignal()

    def __init__(self, project, objectName: str, type, uiFile, ctrlLayout):
        super().__init__(project, objectName, type)
        self._layout = ctrlLayout
        self._connection = Connection(self)
        self._firstPoint = QPoint(1, 1)
        self.origSize = QSize(1, 1)
        self._mousePressed = False
        self._resizeRadius = 5
        self._project = project
        self._lock = False
        self._menu = QMenu(self)
        self._deleteAction = QAction("Delete", self._menu)
        self._lockAction = QAction("Lock", self._menu)
        self._moveUp = QAction("Move Up", self._menu)
        self._moveDown = QAction("Move Down", self._menu)
        self._menu.addActions([self._deleteAction, self._lockAction])
        self._menu.addSeparator()
        self._menu.addActions([self._moveUp, self._moveDown])

        self._deleteAction.triggered.connect(self._deleteTriggered)
        self._lockAction.triggered.connect(self._lockTriggered)
        self._moveUp.triggered.connect(self._moveUpTriggered)
        self._moveDown.triggered.connect(self._moveDownTriggered)

        self._properties.appendPropHead("Geometry Properties", self.geoProperty)
        self._firstTimeProp()

        uic.loadUi(resourcePath(uiFile), self) # Load the .ui file

        self.setObjectName(objectName)

        self._connection.appendCallBack("Set Visible", self._setVisible)
        self._connection.appendCallBack("Set Invisible", self._setInvisible)


    def getConnection(self) -> Connection:
        """
        Returns the _connection object
        :param: none
        :return _connection: Connection object
        """
        return self._connection


    def _setVisible(self):
        self.setVisible(True)


    def _setInvisible(self):
        self.setVisible(False)


    def _moveUpTriggered(self):
        self._layout.moveUp(self)

    
    def _moveDownTriggered(self):
        self._layout.moveDown(self)


    # Override
    def _derPropRequested(self):
        self._properties["Width"] = self.origSize.width()
        self._properties["Height"] = self.origSize.height()
        self._reloadProperty()


    # Override
    def _derPropChanged(self):
        self.move(self._properties["X"], self._properties["Y"])
        self.setFixedSize(self._properties["Width"], self._properties["Height"])
        self.origSize = QSize(self._properties["Width"], self._properties["Height"])

        self.setModLoc(self.origParSize, self.currParSize)
        self.setModSize(self.origParSize, self.currParSize)
        self._reconfProperty()


    # Override
    def contextMenuEvent(self, evt: QContextMenuEvent):
        """
        Brings up the right click menu
        :param evt: Right click event
        :return: none
        """

        self._menu.move(evt.globalX(), evt.globalY())
        self._menu.exec()


    def _deleteTriggered(self):
        self._layout.removeComponent(self)


    def _lockTriggered(self):
        self._lock = not self._lock
        if self._lock:
            self.mouseReleaseEvent(None)
            self._lockAction.setText("Unlock")
        else:
            self._lockAction.setText("Lock")


    # Scenario 1
    def initRatio(self, origSize: QSize, currSize: QSize):
        """
        When the component is first dropped to the layout, we must calculate
        the ratio for location and size to the ctrl layout in order for resizing to work.

        :param origSize: QGeometry object that contains location and size
        """
        self.origSize = self.size()
        self.origParSize = origSize
        self.currParSize = currSize
        self.setLocRatio(currSize)
        self.setSizeRatio(origSize)
        
        self.setModSize(origSize, currSize)


    def setModSize(self, origSize: QSize, currSize: QSize):
        self.setSizeRatio(origSize)

        self.setFixedSize(int(currSize.width() * self.wratio),
         int(currSize.height() * self.hratio))


    def setModLoc(self, origSize: QSize, currSize: QSize):
        self.setLocRatio(origSize)

        self.move(int(currSize.width() * self.xratio), int(currSize.height() * self.yratio))


    def setLocRatio(self, parentGeo: QSize):
        """
        Anytime location is changed, this must be called
        """
        self.xratio = self.x() / parentGeo.width()
        self.yratio = self.y() / parentGeo.height()


    def setSizeRatio(self, parentGeo: QSize):
        """
        Anytime size is changed, this must be called
        """
        self.wratio = self.width() / parentGeo.width()
        self.hratio = self.height() / parentGeo.height()


    def parentResized(self, currSize: QSize):
        aWidth = int(currSize.width() * self.wratio)
        aHeight = int(currSize.height() * self.hratio)
        aX = int(currSize.width() * self.xratio)
        aY = int(currSize.height() * self.yratio)

        self.setFixedSize(aWidth, aHeight)
        self.move(aX, aY)

        self.currParSize = currSize


    # Override
    def mouseMoveEvent(self, evt: QMouseEvent) -> None:
        if (self._mousePressed == True and not self._lock):
            pos = self.mapToParent(evt.pos())
            self.move(pos.x()-self._firstPoint.x(), pos.y()-self._firstPoint.y())
        evt.accept()


    # Override
    def mousePressEvent(self, evt: QMouseEvent) -> None:
        if (self._project.editMode()):
            self.compClicked.emit(self)
            if (not self._lock):
                self.setCursor(Qt.CursorShape.SizeAllCursor)
            self._firstPoint = evt.pos()
            self._mousePressed = True
        evt.accept()

    # Override
    def mouseReleaseEvent(self, evt: QMouseEvent) -> None:
        if (self._project.editMode() and not self._lock):
            self.setCursor(Qt.CursorShape.ArrowCursor)
            self.boundaryCheck(self.pos())
            self.setModLoc(self.currParSize, self.currParSize)
            self._properties["X"] = int(self.origParSize.width() * self.xratio)
            self._properties["Y"] = int(self.origParSize.height() * self.yratio)

            self.attrChanged.emit()
            self._mousePressed = False


    def boundaryCheck(self, pos):
        if (pos.x() <= 0):
            self.move(1, pos.y())

        if (pos.y() <= 0):
            self.move(self.x(), 1)

        if (pos.x() + self.width() >= self.currParSize.width()):
            self.move(self.currParSize.width()-self.width(), self.y())

        if (pos.y() + self.height() >= self.currParSize.height()):
            self.move(self.x(), self.currParSize.height()-self.height())


    # TODO
    '''def cornerResizeCheck(self, pos) -> bool:
        """
        Method for resizing by drag. 
        """
        if (pos.x() <= self._resizeRadius and pos.y() <= self._resizeRadius): # Top Left
            self.setCursor(Qt.CursorShape.SizeFDiagCursor)
        elif (pos.x() >= self.size().width()-self._resizeRadius and pos.y() <= self._resizeRadius): # Top right
            self.setCursor(Qt.CursorShape.SizeBDiagCursor)
        elif (pos.x() <= self._resizeRadius and pos.y() >= self.size().height()-self._resizeRadius): # Bottom right
            self.setCursor(Qt.CursorShape.SizeBDiagCursor)
        elif (pos.x() >= self.size().width()-self._resizeRadius and 
                pos.y() >= self.size().height()-self._resizeRadius): # Bottom left

                newPos = QPoint(pos.x()-self._firstPoint.x(), pos.y()-self._firstPoint.y())
                self.setFixedSize(self.width() + newPos.x(), self.height() + newPos.y())
                self.setCursor(Qt.CursorShape.SizeFDiagCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)'''


    def eventFilter(self, obj: QObject, evt: QEvent) -> bool:
        if (evt.type() == QEvent.Type.MouseMove):
            self.mouseMoveEvent(evt)
        elif (evt.type() == QEvent.Type.MouseButtonPress):
            self.mousePressEvent(evt)
        elif (evt.type() == QEvent.Type.MouseButtonRelease):
            self.mouseReleaseEvent(evt)
        return False 


    @abstractmethod
    def _reconfProperty(self):
        """
        Called when the user modifies any attributes inside the property tab
        :param: none
        :return: none
        """
        pass


    @abstractmethod
    def _reloadProperty(self):
        """
        Reload attributes 
        """
        pass


    @abstractmethod
    def _reconfProperty(self):
        """
        Called when the user modifies any attributes inside the property tab
        :param: none
        :return: none
        """
        pass