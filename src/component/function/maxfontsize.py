from PyQt6.QtGui import QFontMetrics
from PyQt6.QtCore import QRectF

# Copied from https://github.com/jonaias/DynamicFontSizeWidgets/blob/master/src/dynamicfontsizelabel.cpp
# by jonaias

class MaxFontSize:
    @staticmethod
    def maxFontSize(widget, label):
        font = label.font()
        widgetRect = widget.contentsRect()
        widgetWidth = widget.width()
        widgetHeight = widget.height()

        newFontSizeRect = QRectF()

        currSize = font.pointSizeF()
        step = currSize / 2.0

        if (step <= 0.5):
            step = 0.5*4.0

        lastTestedSize = currSize

        currHeight = 0.0
        currWidth = 0.0

        while (step > 0.5 or (currHeight > widgetHeight) or (currWidth > widgetWidth)):
            lastTestedSize = currSize
            font.setPointSizeF(currSize)
            fm = QFontMetrics(font)
            newFontSizeRect = fm.boundingRect(widgetRect, label.alignment(), label.text())

            currHeight = newFontSizeRect.height()
            currWidth = newFontSizeRect.width()

            if ((currHeight > widgetHeight) or (currWidth > widgetWidth)):
                currSize -= step
                if (step > 0.5):
                    step /= 2.0
                if (currSize <= 0):
                    break
            else:
                currSize += step
        
        return lastTestedSize