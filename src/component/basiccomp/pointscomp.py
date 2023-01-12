"""
Developed by: JumpShot Team
Written by: riscyseven
UI designed by: Fisk31
"""

from attr import PropWidgetType, PropInstType, CompPropTemplate
from abstract.displaycomp import DisplayComp
from component.element.counter import Counter
from fileio.fileout import TextOut
from PyQt6.QtCore import Qt

from component.function.maxfontsize import MaxFontSize

class PointsComp(DisplayComp):
    """
    Component that can display a score or period that can be 
    incremented or decremented.
    """

    scoreDispProperty = {
        "Suffix (st, nd, rd, th)": {
            PropInstType.TYPE: PropWidgetType.CHECKBOX,
            PropInstType.VALUE: 0
        },
        "Clr when points = 0": {
            PropInstType.TYPE: PropWidgetType.CHECKBOX,
            PropInstType.VALUE: False
        }
    }

    def __init__(self, project, objectName, parent=None):
        super().__init__(project, objectName, "src/component/basiccomp/pointscomp.ui", parent)

        self.fileOut = TextOut(parent=self)
        self.points = Counter(self.label, self.fileOut, self)

        self.label.setStyleSheet(f"{self.label.styleSheet()}\
            background-color:{self._properties['Background Color']};\
                            color:{self._properties['Font Color']};")

        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)

        self._properties.removeProp("Display Text")
        self._properties.removeProp("Text Alignment")


    # Override
    def _firstTimeProp(self):
        self._properties.appendPropHead("File Properties", CompPropTemplate.fileProperty)
        self._properties.appendPropHead("Points Properties", self.scoreDispProperty)
        self._properties.appendPropHead("Appearance Properties", CompPropTemplate.appearProperty)

        self._connection.appendCallBack("Add Points", self.addPoint)
        self._connection.appendCallBack("Sub Points", self.subPoint)
        self._connection.appendCallBack("Set Points", self.setScore)

        self._properties["Background Color"] = "#242325"
        self._properties["Font Color"] = "#EFCB02"
        self._properties["Font Weight"] = 4


    # Override
    def getName(self) -> str:
        return "Points Display"


    # Override
    def _reloadProperty(self) -> None:
        self._properties["Suffix (st, nd, rd, th)"] = self.points.getSuffix()
        self._properties["File Output Location"] = self.fileOut.getOutputFile()

        self._properties["Display Text"] = self.label.text()
        self._properties["Display Font"] = self.label.font().family()
        self._properties["Font Size"] = self.label.font().pointSize()


    # Override 
    def _reconfProperty(self) -> None:
        self.points.setSuffix(self._properties["Suffix (st, nd, rd, th)"])
        self.points.setValue(self.points.getValue())
        if (self._properties["Enable File Output"]):
            self.fileOut.setOutputFile(self._properties["File Output Location"])
            if (self.fileOut.getOutputFile() != self._properties["File Output Location"]):
                self.attrChanged.emit()
            self.points.enableFileOut(self.fileOut)
        else:
            self.points.disableFileOut()
        self.points.setClearScoreZero(self._properties["Clr when points = 0"])

        font = self.label.font()
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
                self.label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
            case 2:
                self.label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)


    # Override
    def setFileDir(self, dirName):
        if (self._properties["Enable File Output"]):
            self._properties["File Output Location"] = dirName.format(self.objectName())
            self.fileOut.setOutputFile(self._properties["File Output Location"])


    def addPoint(self, value):
        self.points.increment(value)


    def subPoint(self, value):
        self.points.decrement(value)


    def setScore(self, value):
        self.points.setValue(value)


    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        if (self._properties["Auto Font Size"]):
            font = self.label.font()
            font.setPointSizeF(MaxFontSize.maxFontSize(self, self.label))
            self.label.setFont(font)
        a0.accept()