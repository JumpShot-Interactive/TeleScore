"""
Developed by: JumpShot Team
Written by: riscyseven
UI designed by: Fisk31
"""
from abstract.displaycomp import DisplayComp
from fileio.fileout import TextOut
from attr import CompPropTemplate

from component.function.maxfontsize import MaxFontSize

from PyQt6.QtCore import Qt

class TextComp(DisplayComp):
    """
    Text component for scoreboard.
    """

    def __init__(self, project, objectName, parent=None):
        super().__init__(project, objectName, "src/component/basiccomp/textcomp.ui", parent)

        self.fileOut = TextOut(parent=self)

        self.label.setStyleSheet(f"{self.label.styleSheet()}\
            background-color:{self._properties['Background Color']};\
                            color:{self._properties['Font Color']};")

        self._initConn()


    # Override
    def _firstTimeProp(self):
        self._properties.appendPropHead("File Properties", CompPropTemplate.fileProperty)
        self._properties.appendPropHead("Appearance Properties", CompPropTemplate.appearProperty)
        self._properties["Background Color"] = "#404040"
        self._properties["Font Color"] = "#EEEEEE"
        self._properties["Font Weight"] = 4


    # Override
    def getName(self) -> str:
        return "Text Display"


    # Override
    def _reloadProperty(self) -> None:
        self._properties["File Output Location"] = self.fileOut.getOutputFile()
        self._properties["Display Text"] = self.label.text()
        self._properties["Display Font"] = self.label.font().family()
        self._properties["Font Size"] = self.label.font().pointSize()


    # Override
    def _reconfProperty(self):
        if (self._properties["Enable File Output"]):
            if (self.fileOut.getOutputFile() != self._properties["File Output Location"]):
                self.fileOut.setOutputFile(self._properties["File Output Location"])

        font = self.label.font()
        if (not self._properties["Auto Font Size"]):
            font.setPointSize(int(self._properties["Font Size"]))
        font.setWeight(int(self._properties.getValueFromOption("Font Weight")))
        self.label.setFont(font)
        self.label.setStyleSheet(f"background-color:{self._properties['Background Color']};\
                                        font-family:\"{self._properties['Display Font']}\";\
                                        color:{self._properties['Font Color']};")

        if (self._properties["Transparent Background"]):
            self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
            self.label.setStyleSheet(f"{self.label.styleSheet()}background-color:transparent;")
            
        match self._properties["Text Alignment"]:
            case 0:
                self.label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            case 1:
                self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
            case 2:
                self.label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.label.setText(self._properties["Display Text"])


    # Override
    def setFileDir(self, dirName):
        if (self._properties["Enable File Output"]):
            self._properties["File Output Location"] = dirName.format(self.objectName())
            self.fileOut.setOutputFile(self._properties["File Output Location"])


    def _initConn(self):
        self._connection.appendCallBack("Set Text", self._setText)


    def _setText(self, text):
        self.label.setText(text)
        if (self._properties["Enable File Output"]):
            self.fileOut.outputFile(text)


    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        if (self._properties["Auto Font Size"]):
            font = self.label.font()
            font.setPointSizeF(MaxFontSize.maxFontSize(self, self.label))
            self.label.setFont(font)
        a0.accept()