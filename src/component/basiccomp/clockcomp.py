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

from copy import deepcopy

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

        self._initConn()

        self.clockLabel.setStyleSheet(f"{self.clockLabel.styleSheet()}\
                    background-color:{self._properties['Background Color']};\
                                        color:{self._properties['Font Color']};")


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
        super()._firstTimeProp()
        fProp = deepcopy(CompPropTemplate.fileProperty)
        cProp = deepcopy(self.clockProperty)
        apProp = deepcopy(CompPropTemplate.appearProperty)
        advProp = deepcopy(self.advancedProperty)

        fProp["File Output Location"][PropInstType.GET_CALLBACK] = self._getFileProperty
        cProp["Default Time"][PropInstType.GET_CALLBACK] = self._getDefaultTimeProperty
        cProp["Buzzer Sound"][PropInstType.GET_CALLBACK] = self._getBuzzerAudioProperty
        apProp["Display Font"][PropInstType.GET_CALLBACK] = self._getClockFontProperty
        apProp["Font Size"][PropInstType.GET_CALLBACK] = self._getClockFontProperty
        apProp["Font Weight"][PropInstType.GET_CALLBACK] = self._getClockFontProperty

        fProp["Enable File Output"][PropInstType.UPDATE_CALLBACK] = self._enableFileOut
        fProp["File Output Location"][PropInstType.UPDATE_CALLBACK] = self._enableFileOut
        cProp["Stopwatch"][PropInstType.UPDATE_CALLBACK] = self._setStopWatch
        cProp["Format"][PropInstType.UPDATE_CALLBACK] = self._setTimeFormat
        cProp["Default Time"][PropInstType.UPDATE_CALLBACK] = self._setDefaultTime
        cProp["Tenth of a second"][PropInstType.UPDATE_CALLBACK] = self._tenthSec
        cProp["Buzzer Sound"][PropInstType.UPDATE_CALLBACK] = self._setBuzzerAudio
        apProp["Auto Font Size"][PropInstType.UPDATE_CALLBACK] = self._setClockFont
        apProp["Font Size"][PropInstType.UPDATE_CALLBACK] = self._setClockFont
        apProp["Display Font"][PropInstType.UPDATE_CALLBACK] = self._setClockFont
        apProp["Background Color"][PropInstType.UPDATE_CALLBACK] = self._setClockFont
        apProp["Transparent Background"][PropInstType.UPDATE_CALLBACK] = self._setClockFont
        apProp["Font Color"][PropInstType.UPDATE_CALLBACK] = self._setClockFont
        apProp["Font Weight"][PropInstType.UPDATE_CALLBACK] = self._setClockFont
        apProp["Text Alignment"][PropInstType.UPDATE_CALLBACK] = self._setTextAlignment
        advProp["Clock Speed"][PropInstType.UPDATE_CALLBACK] = self._setClockSpeed

        self._properties.appendPropHead("File Properties", fProp)
        self._properties.appendPropHead("Clock Properties", cProp)
        self._properties.appendPropHead("Appearance Properties", apProp)
        self._properties.appendPropHead("Advanced Properties", advProp)

        self._properties.removeProp("Display Text")

        self._properties["Background Color"] = "#242325"
        self._properties["Font Color"] = "#FF9B42"
        self._properties["Font Weight"] = 4

    # --------- Abstract methods -------------

    # Override
    def getName(self) -> str:
        return "Time Display"


    # Override
    def setFileDir(self, dirName):
        if (self._properties["Enable File Output"]):
            self._properties["File Output Location"] = dirName.format(self.objectName())
            self.fileOut.setOutputFile(self._properties["File Output Location"])
    

    # --------- End of abstract methods ----------

    # ---------- Callback methods ----------

    def _tenthSec(self, enable):
        self._stop()
        if (self._properties["Tenth of a second"] and not isinstance(self.clock, ClockMilli)):
            self.clock = ClockMilli(self._stopCallback, False, self.clockLabel, self.fileOut, self)
            self._properties["Clock Speed"] = 100
            self.attrChanged.emit()
        elif (not self._properties["Tenth of a second"] and isinstance(self.clock, ClockMilli)):
            self.clock = Clock(self._stopCallback, False, self.clockLabel, self.fileOut, self)
            self._properties["Clock Speed"] = 1000
            self.attrChanged.emit()


    def _setClockSpeed(self, speed):
        self._stop()
        self.clock.setClockSpeed(speed)
        self.clock.setClockFromStr(self.defaultTime)


    def _setDefaultTime(self, time):
        self._stop()
        self.defaultTime = time
        self.clock.setClockFromStr(self.defaultTime)

    
    def _enableFileOut(self, enable):
        self.clock._stop()
        if (self._properties["Enable File Output"]):
            if (self.fileOut.getOutputFile() != self._properties["File Output Location"]):
                self.fileOut.setOutputFile(self._properties["File Output Location"])
            self.clock.enableFileOut(self.fileOut)
        else:
            self.clock.disableFileOut()


    def _setBuzzerAudio(self, fileName):
        self.clock._stop()
        if (len(self._properties["Buzzer Sound"]) > 0):
            self.audioOutput = QAudioOutput(QMediaDevices.defaultAudioOutput())
            self.audioOutput.setVolume(100)
            self.buzzAudio = QMediaPlayer()
            self.buzzAudio.setAudioOutput(self.audioOutput)
            self.buzzAudio.setSource(QUrl.fromLocalFile(self._properties["Buzzer Sound"]))
        else:
            self.audioOutput = None
            self.buzzAudio = None

    
    def _setTimeFormat(self, format):
        self._stop()
        self.clock.setTimeFormat(self._properties.getValueFromOption("Format"))
        self.clock.setClockFromStr(self.defaultTime)


    def _setStopWatch(self, enable):
        self._stop()
        self.clock.setStopWatch(enable)
        self.clock.setClockFromStr(self.defaultTime)

    
    def _setClearTimeZero(self, enable):
        self._stop()
        self.clock.setClearTimeZero(enable)
        self.clock.setClockFromStr(self.defaultTime)


    def _setClockFont(self, font):
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

        self.clock.setClockFromStr(self.defaultTime)

    def _setTextAlignment(self, align):
        match self._properties["Text Alignment"]:
            case 0:
                self.clockLabel.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            case 1:
                self.clockLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
            case 2:
                self.clockLabel.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)


    def _getFileProperty(self):
        self._properties["File Output Location"] = self.fileOut.getOutputFile()


    def _getDefaultTimeProperty(self):
        self._properties["Default Time"] = self.defaultTime


    def _getBuzzerAudioProperty(self):
        if (self.buzzAudio == None):
            self._properties["Buzzer Audio"] = ""
        else:
            self._properties["Buzzer Audio"] = self.buzzAudio.source().fileName()


    def _getClockFontProperty(self):
        self._properties["Display Font"] = self.clockLabel.font().family()
        self._properties["Font Size"] = self.clockLabel.font().pointSize()


    # ---------- End of Callback functions ----------

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