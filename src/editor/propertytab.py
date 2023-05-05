"""
Developed By: JumpShot Team
Written by: riscyseven
Designed by: Fisk31
"""

from PyQt6.QtWidgets import QWidget
from PyQt6 import uic
from PyQt6.QtCore import QModelIndex, pyqtSignal

from property.property.property import Property
from editor.proptab.propwidgethead import PropWidgetHead
from editor.proptab.propwidgetitem import PropWidgetItem
from gm_resources import resourcePath

class PropertyTab(QWidget):
    """
    Widget that displays the properties information for a component
    """

    propChanged = pyqtSignal()

    def __init__(self, propertyQueue, parent=None):
        super().__init__(parent) # Call the inherited classes __init__ method
        uic.loadUi(resourcePath("src/editor/propertytab.ui"), self) # Load the .ui file

        self.treeWidget.setAlternatingRowColors(True)
        self.treeWidget.setProperty("class", "PropListView")

        self._properties = None
        self._propertyQueue = propertyQueue


    def clearTree(self):
        while self.treeWidget.topLevelItemCount() > 0:
            head = self.treeWidget.takeTopLevelItem(0)
            while head.childCount() > 0:
                item = head.takeChild(0)
                item.deleteWidget()
                item = None
            head = None


    def resizeEvent(self, evt) -> None:
        """
        Anytime the treeview is resized, this is called to have
        each column to be sized proportionately. 

        :param evt: resize event information
        :return: none
        """
        width = self.treeWidget.width() // self.treeWidget.columnCount()
        self.treeWidget.header().resizeSection(0, width) 
        evt.accept()
    
    
    def loadProperties(self, properties):
        self._properties = properties
        self._parseProperties()


    def _parseProperties(self):
        for i, headName in enumerate(self._properties.getCategorizedProperties()):
            header = PropWidgetHead(headName, self.treeWidget)
            # This sets the header to span all the columns
            self.treeWidget.setFirstColumnSpanned(i, QModelIndex(), True)

            for prop in self._properties[headName]:           
                tabItem = PropWidgetItem(header, prop, self._propItemChanged, self.treeWidget)
                self.treeWidget.setItemWidget(tabItem, 1, tabItem.getWidget())
            header.setExpanded(True) # Making sure the tabs are expanded


    def _propInstChanged(self, prop, value):
        newProp = Property(prop.getName(), prop.getType(),
                            value, prop.getOption(), prop.getCallback())
        self._propertyQueue.append(prop, newProp)


    def externalChange(self):
        self.clearTree()
        self._parseProperties()
        