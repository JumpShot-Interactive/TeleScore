"""
Developed by: JumpShot Team
Written by: riscyseven
UI designed by: Fisk31
"""

from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt

from attr import CompPropTemplate
from abstract.controlcomp import ControlComp
from component.hotkey import HotKey

class ButtonComp(ControlComp):
    """
    Button widget for scoreboard.
    """
    
    def __init__(self, project, type, text, signal: str, objectName, parent=None):
        super().__init__(project, objectName, "src/component/basiccomp/buttoncomp.ui", parent)

        self.signal = signal
        self.buttonType = type
        self.text = text
        self.hotKey = None
        self.pushButton.setText(text)
        self.pushButton.clicked.connect(self._onClick)
        self._connection.appendConnType(self.signal)
        self._properties.removeProp("Text Alignment")
        self._properties.removeProp("Auto Font Size")

        if (project.inEditor()):
            self.pushButton.installEventFilter(self) # This might cause performance issues

    # Override
    def _firstTimeProp(self):
        self._properties.appendPropHead("Appearance Properties", CompPropTemplate.appearProperty)
        self._properties.appendPropHead("Hotkey Properties", CompPropTemplate.hotkeyProperty)
        self._properties["Font Color"] = "#FFFFFF"
        self._properties["Font Weight"] = 1


    # Override
    def _reloadProperty(self):
        self._properties["Display Text"] = self.pushButton.text()
        self._properties["Display Font"] = self.pushButton.font().family()
        self._properties["Font Size"] = self.pushButton.font().pixelSize()


    # Override
    def _reconfProperty(self):
        self.pushButton.setStyleSheet(f"QPushButton{{color:{self._properties['Font Color']};\
                                        font-size:{self._properties['Font Size']}px;\
                                        font-weight:{self._properties.getValueFromOption('Font Weight')};\
                                        font-family:\"{self._properties['Display Font']}\";}}")

        self.setButtonColor(self._properties["Background Color"])

        if (self._properties["Transparent Background"]):
            self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
            self.pushButton.setStyleSheet(f"{self.pushButton.styleSheet()}QPushButton{{background-color:transparent;}}")

        self.pushButton.setText(self._properties["Display Text"])

        if (self.hotKey != None):
            self.hotKey.signal.disconnect(self._onClick)
            self.hotKey.stopThread()
            self.hotKey = None
        if (self._properties["Hotkey"] != ""):    
            self.hotKey = HotKey(self._properties["Hotkey"])
            self.hotKey.signal.connect(self._onClick)


    # Override
    def getName(self) -> str:
        return self.buttonType


    # Override
    def setEditorMode(self, mode):
        self.pushButton.installEventFilter(self) if mode else self.pushButton.removeEventFilter(self)


    def _onClick(self):
        self._connection.emitSignal(self.signal)


    def setButtonColor(self, hexval: str):
        """
        Method that automatically determines the button colour for hover
        and press actions.

        :param hexval: String hex value "#ffffff"
        :return: None
        """
        dimmed = QColor(hexval)
        dimmed.setRgb(dimmed.red() // 2, dimmed.green() // 2, dimmed.blue() // 2)

        self.pushButton.setStyleSheet(f"{self.pushButton.styleSheet()}\
                                        QPushButton{{background-color:{hexval};}}\
                                        QPushButton:pressed{{background-color:{dimmed.name(QColor.NameFormat.HexRgb)};}}")

        self._properties["Background Color"] = hexval

