"""
Developed by: JumpShot Team
Written by: riscyseven
"""

from PyQt6.QtCore import QObject, pyqtSignal, QTimer, QTime, pyqtSlot
from time import time

class Clock(QObject):
    """
    Class that implements a basic clock (timer or stopWatch),
    Utitlizes QTimer for the clock to update. 
    For cleaner code, QTimer is updated every milliseconds
    instead of seconds.
    """

    clkChngedSignal = pyqtSignal(str) # Signal/Callback for when clock is changed

    def __init__(self, stopCallBack, stopWatch=False, label=None, file=None, parent=None):
        """
        """
        super(QObject, self).__init__(parent)
        self.tick = 0
        self.clock = QTimer()
        self.speed = 1000 
        self.tickTo = 0
        self.__stopWatch = stopWatch
        self.file = file
        self.clearZero = False
        self.carryOver = False
        self.timeFormat = "mm:ss"
        self._stopCallback = stopCallBack
        self._start = 0

        self.label = label
        self.clearTimeZero = False

        self.clock.timeout.connect(self._clockEvent)

    def enableFileOut(self, file):
        self.file = file

    def disableFileOut(self):
        self.file = None

    def getTick(self) -> int:
        return self.tick

    def setTimeFormat(self, value):
        if (value.lower().count("h") > 0):
            self.carryOver = True
        else:
            self.carryOver = False
        self.timeFormat = value

    def setStopWatch(self, value: bool):
        self.__stopWatch = value


    def setClockSpeed(self, speed):
        self.speed = speed


    def getTimeFormat(self):
        return self.timeFormat


    def stopClock(self):
        self.clock.stop()


    def startClock(self):
        if (not self.clock.isActive()):
            if (self.__stopWatch):
                self._start = int(time()-self.tick)
            else:
                self._start = int(time()+self.tick+1)
            self.clock.start(self.speed)


    def startStopClock(self):
        if (self.clock.isActive()):
            self.startClock()
        else:
            self.stopClock()


    def _valueChanged(self):
        timeStr = self._convTicktoStr(self.tick, self.timeFormat)

        if (self.clearTimeZero and self.tick <= 0):
            timeStr = ""

        if (self.label != None):
            self.label.setText(timeStr)
        if (self.file != None):
            self.file.outputFile(timeStr)
        self.clkChngedSignal.emit(timeStr)


    def _stopWatch(self):
        self.tick = int(time()-self._start)
        self._valueChanged()


    def _timer(self):
        self.tick = int(self._start-time())

        if (self.tick <= 0):
            self.tick = 0
            self._valueChanged()
            self._stopCallback()
            self.stopClock()
        else:
            self._valueChanged()


    def setClockTick(self, tick):
        if (tick >= 0 and tick < 432000):
            self.tick = tick
            if (self.clock.isActive()):
                self.stopClock()
                self.startClock()
            self._valueChanged()


    def addTime(self, min, sec):
        tempTick = self.tick + min * 60 + sec
        self.setClockTick(tempTick)


    def setClockFromStr(self, str, timeFormat=None) -> bool:
        if (timeFormat == None):
            timeFormat = self.timeFormat
        time = QTime.fromString(str, timeFormat)
        if (time.isValid()):
            self.setClockTick(time.hour()*3600+time.minute()*60+time.second())
        else:
            self._valueChanged()
        return time.isValid()


    def setClearTimeZero(self, value):
        self.clearTimeZero = value


    @pyqtSlot()
    def _clockEvent(self):
        if (self.__stopWatch):
            self._stopWatch()
        else:
            self._timer()
    

    def _convTicktoStr(self, tick: int, timeFormat: str) -> str:
        dict = {}
        dict["s"] = tick % 60
        dict["m"] = (tick // 60) % 60
        if (not self.carryOver):
            dict["m"] = (tick // 60)
        dict["h"] = (tick // 3600) % 24

        lastPos = 0
        currChar = ''
        newStr = ""
        timeFormat = f"{timeFormat} "

        for currPos, i in enumerate(timeFormat):
            if (currChar != i):
                if (currChar in dict):
                    pos = currPos-lastPos
                    newStr = f"{newStr}{dict[currChar]:0{pos}d}"
                else:
                    newStr = f"{newStr}{currChar}"
                currChar = i
                lastPos = currPos

        return newStr

    def isRunning(self) -> bool:
        return self.clock.isActive()