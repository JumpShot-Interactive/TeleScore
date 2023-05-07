"""
Developed By: JumpShot Team
Written by: riscyseven
"""

from PyQt6.QtWidgets import QDialog
from PyQt6 import uic

from editor.proptab.propwidgetitem import PropWidgetItem
from editor.proptab.proplineedit import PropLineEdit
from property.properties import Properties
from gm_resources import resourcePath

class Settings(QDialog):
    def __init__(self, property, parent=None):
        super().__init__(parent) # Call the inherited classes __init__ method
        self.property: Properties = property
        self._properties = self.property.getPropertyDict()
        self._initUI()
        self.tempChanges = {}


    def _initUI(self) -> None:
        """
        Initializes the settings UI.

        :param: none
        :return: none
        """
        path = resourcePath("src/window/ui/settings.ui")
        uic.loadUi(path, self) # Load the .ui file
        self.treeWidget.setProperty("class", "SettTreeView")
        self.listWidget.setProperty("class", "SettListWidget")
        self.treeWidget.setAlternatingRowColors(True)
        self._parseProperties()
        self.listWidget.itemClicked.connect(self._tabChanged)
        self.buttonBox.clicked.connect(self._buttonClicked)
        self.buttonBox.button(self.buttonBox.StandardButton.Apply).setEnabled(False)

        if (self.listWidget.count() > 0):
            self.listWidget.setCurrentRow(0)
            self._tabChanged(self.listWidget.item(0))


    def _buttonClicked(self, button):
        if (button == self.buttonBox.button(self.buttonBox.StandardButton.Ok)):
            self.applySettings()
            self.accept()
        elif (button == self.buttonBox.button(self.buttonBox.StandardButton.Apply)):
            self.applySettings()
        else:
            self.reject()


    def applySettings(self):
        self.buttonBox.button(self.buttonBox.StandardButton.Apply).setEnabled(False)
        for prop, value in self.tempChanges.items():
            prop.setValue(value)


    def _clearTree(self):
        while self.treeWidget.topLevelItemCount() > 0:
            item = self.treeWidget.takeTopLevelItem(0)
            item.deleteWidget()
            del item


    def _tabChanged(self, item) -> None:
        self._clearTree()

        for prop in self.property.getPropertyDict()[item.text()]:           
            tabItem = PropWidgetItem(self.treeWidget, prop, self._propItemChanged)
            if (isinstance(tabItem.getWidget(), PropLineEdit)):
                tabItem.getWidget().propertyMode() # Janky changed this in thje future
            self.treeWidget.setItemWidget(tabItem, 1, tabItem.getWidget())


    def resizeEvent(self, evt) -> None:
        """
        Anytime the treeview is resized, this is called to have
        each column to be sized proportionately. 

        :param evt: resize event information
        :return: none
        """
        width = self.treeWidget.width() // self.treeWidget.columnCount()

        self.treeWidget.header().resizeSection(0, width)         


    def _propItemChanged(self, prop, value):
        self.tempChanges[prop] = value
        self.buttonBox.button(self.buttonBox.StandardButton.Apply).setEnabled(True)


    def _parseProperties(self):
        propList = self.property.getPropertyDict()
        for tabName in propList:
            self.listWidget.addItem(tabName)