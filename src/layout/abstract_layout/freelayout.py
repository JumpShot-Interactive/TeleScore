"""
Developed By: JumpShot Team
Written by: riscyseven
"""

# This Python file uses the following encoding: utf-8
from PyQt6.QtWidgets import QLayout
from PyQt6.QtCore import QSize, QRect

class FreeLayout(QLayout):
    """
    New QLayout subclass that enables the component/widgets
    to be placed any where in the layout without any restrictions.
    """

    def __init__(self, size: QSize, parent=None):
        super().__init__(parent)
        self.items = [] # QLayoutItem List
        self.size = size
        self.setGeometry(QRect(0, 0, size.width(), size.height()))


    # Override
    def addItem(self, item) -> None:
        self.items.append(item)


    # Override
    def count(self) -> None:
        return len(self.items)


    # Override
    def itemAt(self, index) -> None:
        if (index < self.count()):
            return self.items[index]
        return None


    # Override
    def takeAt(self, index):
        item = self.items[index]
        self.items.remove(item)
        return item


    # Override
    def sizeHint(self):
        return self.size


    def getLOWidgets(self) -> list:
        tempList = []
        for comp in self.items:
            tempList.append(comp.widget())
        return tempList


    def moveUp(self, comp):
        index = self.indexOf(comp)
        if (index + 1 < self.count()):
            aboveIndex = index + 1
            self.items[aboveIndex].widget().stackUnder(comp)
            self.items[index], self.items[aboveIndex] = self.items[aboveIndex], self.items[index]


    def moveDown(self, comp):
        index = self.indexOf(comp)
        if (index - 1 >= 0):
            aboveIndex = index - 1
            comp.stackUnder(self.items[aboveIndex].widget())
            self.items[index], self.items[aboveIndex] = self.items[aboveIndex], self.items[index]

