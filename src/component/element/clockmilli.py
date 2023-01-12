"""
Developed by: JumpShot Team
Written by: riscyseven
"""

from PyQt6.QtCore import QTime
from PyQt6.QtWidgets import QLabel

from component.element.clock import Clock
from fileio.fileout import TextOut

from time import time

class ClockMilli(Clock):
    """
    Class that implements a basic clock (timer or stopwatch),
    Utitlizes QTimer for the clock to update. 
    For cleaner code, QTimer is updated every milliseconds
    instead of seconds.
    """

    def __init__(self, stopCallBack, stopWatch=False, label: QLabel=None, file:TextOut=None, parent=None):
        """
        """
        super().__init__(stopCallBack, stopWatch, label, file, parent)
        self.speed = 100


    # Override
    def addTime(self, min, sec):
        tempTick = self.tick+min*600+sec*10
        self.setClockTick(tempTick)

    
    # Override
    def startClock(self):
        if (not self.clock.isActive()):
            if (self._Clock__stopWatch):
                self._start = int(time()*10)-self.tick
            else:
                self._start = int(time()*10)+self.tick
            self.clock.start(self.speed)


    # Override
    def setClockFromStr(self, str, timeFormat=None) -> bool:
        if (timeFormat == None):
            timeFormat = self.timeFormat
        time = QTime.fromString(str, timeFormat)
        if (time.isValid()):
            self.setClockTick(time.hour()*36000+time.minute()*600+time.second()*10+time.msec()//100)
        else:
            self._valueChanged()
        return time.isValid()

    
    def _stopWatch(self):
        self.tick = int(time()*10)-self._start
        self._valueChanged()


    def _timer(self):
        self.tick = self._start-int(time()*10)

        if (self.tick <= 0):
            self.tick = 0
            self._valueChanged()
            self._stopCallback()
            self.stopClock()
        else:
            self._valueChanged()

    
    # Override
    def _valueChanged(self):
        timeStr = ""
        if (self.tick < 600 and not self._Clock__stopWatch):
            timeStr = self._convTicktoStr(self.tick, "ss.z")
        else:
            timeStr = self._convTicktoStr(self.tick, self.timeFormat)

        if (self.label != None):
            self.label.setText(timeStr)
        if (self.file != None):
            if (self.clearTimeZero and self.tick <= 0):
                timeStr = ""
            self.file.outputFile(timeStr)
        self.clkChngedSignal.emit(timeStr)


    # Override
    def _convTicktoStr(self, tick: int, timeFormat: str) -> str:
        dict = {}
        dict["z"] = tick % 10
        dict["s"] = (tick // 10) % 60
        dict["m"] = (tick // 600) % 60
        if (not self.carryOver):
            dict["m"] = (tick // 600)
        dict["h"] = (tick // 36000) % 24

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