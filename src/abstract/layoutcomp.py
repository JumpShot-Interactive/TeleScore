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

    TOP_LEFT = 1
    TOP_RIGHT = 2
    BOTTOM_LEFT = 3
    BOTTOM_RIGHT = 4

    compClicked = pyqtSignal(object)
    attrChanged = pyqtSignal()

    def __init__(self, project, objectName: str, type, uiFile, ctrlLayout):
        super().__init__(project, objectName, type)
        self._layout = ctrlLayout
        self._connection = Connection(self)
        self._firstPoint = QPoint(1, 1)
        self._firstPointParent = QPoint(1, 1)
        self._firstSize = QSize(1, 1)
        self.origSize = QSize(1, 1)
        self._mousePressed = False
        self._mouseResized = 0
        self._resizeRadius = 20
        self._project = project
        self._menu = QMenu(self)
        self._menu.setStyleSheet("QMenu {background-color: #2d2d2d;}")
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
        self._properties["Lock"] = False
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

        self.setModLoc(self._layout.getProjSize(), self._layout.getCurrSize())
        self.setModSize(self._layout.getProjSize(), self._layout.getCurrSize())
        self._reconfProperty()
        #self.setToolTip(self.objectName())
        
        if self._properties["Lock"]:
            self._lockAction.setText("Unlock")


    # Override
    def contextMenuEvent(self, evt: QContextMenuEvent):
        """
        Brings up the right click menu
        :param evt: Right click event
        :return: none
        """
        if (self._project.inEditor()):
            self._menu.move(evt.globalX(), evt.globalY())
            self._menu.exec()


    def _deleteTriggered(self):
        self._layout.removeComponent(self)


    def _lockTriggered(self):
        self._properties["Lock"] = not self._properties["Lock"]
        if self._properties["Lock"]:
            self.mouseReleaseEvent(None)
            self._lockAction.setText("Unlock")
        else:
            self._lockAction.setText("Lock")


    def initRatio(self, origSize: QSize, currSize: QSize):
        """
        When the component is first dropped to the layout, we must calculate
        the ratio for location and size to the ctrl layout in order for resizing to work.

        :param origSize: QGeometry object that contains location and size
        """
        self.origSize = self.size()
        self.setLocRatio(currSize)
        self.setSizeRatio(origSize)
        
        self.setModSize(origSize, currSize)


    def setModSize(self, origSize: QSize, currSize: QSize):
        self.setSizeRatio(origSize)
        self.setFixedSize(round(currSize.width() * self.wratio),
         round(currSize.height() * self.hratio))


    def setModLoc(self, origSize: QSize, currSize: QSize):
        self.setLocRatio(origSize)

        self.move(round(currSize.width() * self.xratio), round(currSize.height() * self.yratio))


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
        aWidth = round(currSize.width() * self.wratio)
        aHeight = round(currSize.height() * self.hratio)
        aX = round(currSize.width() * self.xratio)
        aY = round(currSize.height() * self.yratio)

        self.setFixedSize(aWidth, aHeight)
        self.move(aX, aY)


    def _mouseResize(self, pos):
        firstPoint = self._firstPoint

        sizeList = [
            QSize(self._firstSize.width() + firstPoint.x() - pos.x(),
                    self._firstSize.height() + firstPoint.y() - pos.y()),
            QSize(pos.x() - firstPoint.x() + self._firstSize.width(),
                    self._firstSize.height() + firstPoint.y() - pos.y()),
            QSize(self._firstSize.width() + firstPoint.x() - pos.x(),
                    pos.y() - firstPoint.y() + self._firstSize.height()), 
            QSize(pos.x() - firstPoint.x() + self._firstSize.width(),
                    pos.y() - firstPoint.y() + self._firstSize.height())
        ]

        moveList = [
            QPoint(pos.x(), pos.y()),
            QPoint((firstPoint.x()-self._firstSize.width()), pos.y()),
            QPoint(pos.x(), (firstPoint.y()-self._firstSize.height())),
            QPoint((firstPoint.x()-self._firstSize.width()), (firstPoint.y()-self._firstSize.height()))
        ]

        if (sizeList[self._mouseResized-1].width() > 30 and
            sizeList[self._mouseResized-1].height() > 30):
            self.setFixedSize(sizeList[self._mouseResized-1])
            self.move(moveList[self._mouseResized-1])


    # Override
    def mouseMoveEvent(self, evt: QMouseEvent) -> None:
        if (self._mousePressed == True and not self._properties["Lock"]):
            pos = self.mapToParent(evt.pos())
            if (not self._mouseResized):
                self.move(pos.x()-self._firstPoint.x(), pos.y()-self._firstPoint.y())
            else:
                self._mouseResize(pos)
        evt.accept()


    # Override
    def mousePressEvent(self, evt: QMouseEvent) -> None:
        if (evt.button() == Qt.MouseButton.LeftButton and self._project.editMode()):
            self.compClicked.emit(self)
            self._mouseResized = self.cornerResizeCheck(evt.pos())
            self._firstPoint = evt.pos()
            self._firstSize = self.size()
            self._mousePressed = True

            pointList = [self.pos(),
                        QPoint(self.pos().x()+self.width(), self.pos().y()),
                        QPoint(self.pos().x(), self.pos().y()+self.height()),
                        QPoint(self.pos().x()+self.width(), self.pos().y()+self.height())]

            if (self._mouseResized):
                self._firstPoint = pointList[self._mouseResized-1]

            if (not self._properties["Lock"]):
                match self._mouseResized:
                    case self.TOP_LEFT | self.BOTTOM_RIGHT:
                        self.setCursor(Qt.CursorShape.SizeFDiagCursor)
                    case self.TOP_RIGHT | self.BOTTOM_LEFT:
                        self.setCursor(Qt.CursorShape.SizeBDiagCursor)
                    case _:
                        self.setCursor(Qt.CursorShape.SizeAllCursor)
        evt.accept()

    # Override
    def mouseReleaseEvent(self, evt: QMouseEvent) -> None:
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self._mousePressed = False
        if (self._project.editMode() and not self._properties["Lock"]):
            self.setModLoc(self._layout.getCurrSize(), self._layout.getCurrSize())
            self._properties["X"] = round(self._layout.getProjSize().width() * self.xratio)
            self._properties["Y"] = round(self._layout.getProjSize().height() * self.yratio)

            if (self._mouseResized):
                self.setSizeRatio(self._layout.getCurrSize())
                self.setLocRatio(self._layout.getCurrSize())
                self._properties["Width"] = round(self._layout.getProjSize().width() * self.wratio)
                self._properties["Height"] = round(self._layout.getProjSize().height() * self.hratio)
                self.origSize = QSize(self._properties["Width"], self._properties["Height"])
                self._mouseResized = 0
            
            self.attrChanged.emit()

        if (evt is not None):
            evt.accept()


    def cornerResizeCheck(self, pos) -> bool:
        """
        Check to see if the mouse is in the corner of the component
        """
        width = self.size().width()
        height = self.size().height()
        x = pos.x()
        y = pos.y()
        location = [
            [QPoint(0, 0), QPoint(self._resizeRadius, self._resizeRadius)],
            [QPoint(width-self._resizeRadius, 0), QPoint(width, self._resizeRadius)],
            [QPoint(0, height-self._resizeRadius), QPoint(self._resizeRadius, height)],
            [QPoint(width-self._resizeRadius, height-self._resizeRadius), QPoint(width, height)]
        ]

        for i, loc in enumerate(location):
            if (loc[0].x() <= x <= loc[1].x() and loc[0].y() <= y <= loc[1].y()):
                return i + 1

        return 0


    def eventFilter(self, obj: QObject, evt: QEvent) -> bool:
        if (evt.type() == QEvent.Type.MouseMove):
            self.mouseMoveEvent(evt)
            return True
        elif (evt.type() == QEvent.Type.MouseButtonPress):
            self.mousePressEvent(evt)
        elif (evt.type() == QEvent.Type.MouseButtonRelease):
            self.mouseReleaseEvent(evt)
        else:
            return super().eventFilter(obj, evt)

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