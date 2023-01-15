"""
Developed by: JumpShot Team
Written by: riscyseven
UI designed by: Fisk31
"""

from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput, QMediaDevices
from PyQt6.QtCore import QUrl, Qt

from attr import PropWidgetType, PropInstType, CompPropTemplate
from abstract.displaycomp import DisplayComp
from component.element.clock import Clock
from component.element.clockmilli import ClockMilli
from fileio.fileout import TextOut
from component.function.maxfontsize import MaxFontSize


class ClockComp(DisplayComp):
    """
    CLock widget for scoreboard.

    This class has one clock object from the backend.
    """

    clockProperty = {
        "Stopwatch": {
            PropInstType.TYPE: PropWidgetType.CHECKBOX,
            PropInstType.VALUE: False
        },
        "Format": {
            PropInstType.TYPE: PropWidgetType.COMBOBOX,
            PropInstType.VALUE: 0,
            PropInstType.OPTION: ["mm:ss", "hh:mm:ss", "m:ss", "mm", "ss", "hh", "mm:ss.z", "hh:mm:ss.z", "ss.z"],
        },
        "Default Time": {
            PropInstType.TYPE: PropWidgetType.TEXTEDIT,
            PropInstType.VALUE: "00:00"
        },
        "Clr when time = 0": {
            PropInstType.TYPE: PropWidgetType.CHECKBOX,
            PropInstType.VALUE: False
        },
        "Buzzer Sound": {
            PropInstType.TYPE: PropWidgetType.FLOPEN,
            PropInstType.VALUE: ""
        },
        "Tenth of a second": {
            PropInstType.TYPE: PropWidgetType.CHECKBOX,
            PropInstType.VALUE: False
        },
    }

    advancedProperty = {
        "Clock Speed": {
            PropInstType.TYPE: PropWidgetType.NUMEDIT,
            PropInstType.VALUE: 1000,
        }
    }

    def __init__(self, project, objectName, parent=None):
        super().__init__(project, objectName, "src/component/basiccomp/clockcomp.ui", parent)

        self.fileOut = TextOut(parent=self)
        self.clock = Clock(self._stopCallback, False, self.clockLabel, self.fileOut, self)
        self.defaultTime = "00:00"
        self.buzzAudio = None


        self.clockLabel.setStyleSheet(f"{self.clockLabel.styleSheet()}\
                    background-color:{self._properties['Background Color']};\
                                        color:{self._properties['Font Color']};")

        self._properties.removeProp("Display Text")

        self._initConn()


    def _initConn(self):
        self._connection.appendConnType("Clock Stop")
        self._connection.appendCallBack("Start", self._start)
        self._connection.appendCallBack("Stop", self._stop)
        self._connection.appendCallBack("Reset", self._reset)
        self._connection.appendCallBack("Set Time", self._setTime)

        self._connection.appendCallBack("ADDS", self._addSec)
        self._connection.appendCallBack("ADDM", self._addMin)
        self._connection.appendCallBack("SUBS", self._subSec)
        self._connection.appendCallBack("SUBM", self._subMin)
        self._connection.appendCallBack("Clock Stop", self._stop)


    # Override
    def _firstTimeProp(self):
        self._properties.appendPropHead("File Properties", CompPropTemplate.fileProperty)
        self._properties.appendPropHead("Clock Properties", self.clockProperty)
        self._properties.appendPropHead("Appearance Properties", CompPropTemplate.appearProperty)
        self._properties.appendPropHead("Advanced Properties", self.advancedProperty)
        self._properties["Background Color"] = "#242325"
        self._properties["Font Color"] = "#FF9B42"
        self._properties["Font Weight"] = 4


    # Override
    def getName(self) -> str:
        return "Time Display"


    # Override
    def _reloadProperty(self) -> None:
        self._properties["Default Time"] = self.defaultTime
        self._properties["File Output Location"] = self.fileOut.getOutputFile()
        if (self.buzzAudio == None):
            self._properties["Buzzer Audio"] = ""
        else:
            self._properties["Buzzer Audio"] = self.buzzAudio.source().fileName()

        self._properties["Display Font"] = self.clockLabel.font().family()
        self._properties["Font Size"] = self.clockLabel.font().pointSize()
        self._properties["Bold"] = self.clockLabel.font().weight()


    # Override
    def _reconfProperty(self):
        self.clock.stopClock()
        if (self._properties["Tenth of a second"] and not isinstance(self.clock, ClockMilli)):
            self.clock = ClockMilli(self._stopCallback, False, self.clockLabel, self.fileOut, self)
            self._properties["Clock Speed"] = 100
            self.attrChanged.emit()
        elif (not self._properties["Tenth of a second"] and isinstance(self.clock, ClockMilli)):
            self.clock = Clock(self._stopCallback, False, self.clockLabel, self.fileOut, self)
            self._properties["Clock Speed"] = 1000
            self.attrChanged.emit()

        self.clock.setClockSpeed(self._properties["Clock Speed"])

        self.defaultTime = self._properties["Default Time"]
        if (self._properties["Enable File Output"]):
            self.fileOut.setOutputFile(self._properties["File Output Location"])
            if (self.fileOut.getOutputFile() != self._properties["File Output Location"]):
                self.attrChanged.emit()
            self.clock.enableFileOut(self.fileOut)
        else:
            self.clock.disableFileOut()

        self.clock.setTimeFormat(self._properties.getValueFromOption("Format"))
        self.clock.setStopWatch(self._properties["Stopwatch"])
        self.clock.setClearTimeZero(self._properties["Clr when time = 0"])

        self.clock.setClockFromStr(self.defaultTime)

        if (len(self._properties["Buzzer Sound"]) > 0):
            self.audioOutput = QAudioOutput(QMediaDevices.defaultAudioOutput())
            self.audioOutput.setVolume(100)
            self.buzzAudio = QMediaPlayer()
            self.buzzAudio.setAudioOutput(self.audioOutput)
            self.buzzAudio.setSource(QUrl.fromLocalFile(self._properties["Buzzer Sound"]))
        else:
            self.audioOutput = None
            self.buzzAudio = None

        font = self.clockLabel.font()
        if (not self._properties["Auto Font Size"]):
            font.setPointSize(int(self._properties["Font Size"]))
        font.setWeight(int(self._properties.getValueFromOption("Font Weight")))
        self.clockLabel.setFont(font)
        self.clockLabel.setStyleSheet(f"background-color:{self._properties['Background Color']};\
                                        font-family:\"{self._properties['Display Font']}\";\
                                        color:{self._properties['Font Color']};")


        if (self._properties["Transparent Background"]):
            self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
            self.clockLabel.setStyleSheet(f"{self.clockLabel.styleSheet()}background-color:transparent;")


        match self._properties["Text Alignment"]:
            case 0:
                self.clockLabel.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            case 1:
                self.clockLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
            case 2:
                self.clockLabel.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)


    # Override
    def setFileDir(self, dirName):
        if (self._properties["Enable File Output"]):
            self._properties["File Output Location"] = dirName.format(self.objectName())
            self.fileOut.setOutputFile(self._properties["File Output Location"])


    def _start(self):
        self.clock.startClock()


    def _stop(self):
        self.clock.stopClock()


    def _setTime(self, value):
        self.clock.setClockFromStr(value[0], value[1])


    def _reset(self):
        self.clock.setClockFromStr(self.defaultTime)
        if (self.buzzAudio != None):
            self.buzzAudio.stop()


    def _addSec(self):
        self.clock.addTime(0, 1)


    def _addMin(self):
        self.clock.addTime(1, 0)


    def _subSec(self):
        self.clock.addTime(0, -1)


    def _subMin(self):
        self.clock.addTime(-1, 0)


    def _stopCallback(self):
        if (self.buzzAudio != None):
            self.buzzAudio.play()
        self._connection.emitSignal("Clock Stop")
    

    def resizeEvent(self, a0) -> None:
        super().resizeEvent(a0)
        
        if (self._properties["Auto Font Size"]):
            font = self.clockLabel.font()
            font.setPointSizeF(MaxFontSize.maxFontSize(self, self.clockLabel))
            self.clockLabel.setFont(font)