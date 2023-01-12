"""
Developed By: JumpShot Team
Written by: riscyseven
Designed by: Fisk31
"""

# This Python file uses the following encoding: utf-8
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QDrag
from PyQt6.QtCore import QMimeData, Qt, QByteArray, QModelIndex
from PyQt6 import uic

from attr import CompAttr, CompList
from gm_resources import resourcePath
from editor.comptab.compwidgethead import CompWidgetHead
from editor.comptab.compwidgetitem import CompWidgetItem


class CompListTab(QWidget):
    """
    Widget that displays all of the components for the scoreboard. 
    """
    
    def __init__(self, parent=None):
        super().__init__(parent) # Call the inherited classes __init__ method
        path = resourcePath("src/editor/complisttab.ui")
        uic.loadUi(path, self) # Load the .ui file

        self.loadTabs()
        self.treeWidget.itemPressed.connect(self.compItemClicked)
        self.treeWidget.setProperty("class", "CompListView")
        self.treeWidget.setAlternatingRowColors(True)
        self.treeWidget.header().resizeSection(0, 240) 
        self.treeWidget.header().resizeSection(1, 30)


    def loadTabs(self) -> None:
        """
        Loads the category tab.

        :param: none
        :return: none
        """
        for i, cat in enumerate(CompList.category):
            header = CompWidgetHead(cat[CompAttr.TABNAME], self.treeWidget)
            self.treeWidget.setFirstColumnSpanned(i, QModelIndex(), True)
            for name, comp in cat[CompAttr.COMPONENT].items():  # Refractor this please
                iconPath = resourcePath(comp[CompAttr.ICON])
                component = CompWidgetItem(iconPath, name, comp[CompAttr.HELP], header, self.treeWidget)
                self.treeWidget.setItemWidget(component, 1, component.get_infoButton())

            header.setExpanded(True)

    def compItemClicked(self, item: CompWidgetItem, column: int) -> None:
        """
        Initiates drag support

        :param index: Item that is clicked
        :return: none
        """
        if (type(item) != CompWidgetHead):
            mimeData = QMimeData()
            convByte = str.encode(item.text(0))
            mimeData.setData("application/x-comp", QByteArray(convByte))
            drag = QDrag(self)
        
            drag.setMimeData(mimeData)
            drag.setPixmap(item.icon(0).pixmap(20, 20))
            drag.exec(Qt.DropAction.MoveAction | Qt.DropAction.CopyAction)



