
"""
Developed By: JumpShot Team
Written by: riscyseven
"""

from PyQt6.QtWidgets import QWidget
from PyQt6 import uic

from editor.actitab.activecompitem import ActiveCompItem
from project import Project
from gm_resources import resourcePath

class ActiveTab(QWidget):
    """
    Widget that displays the properties information for a component
    """
    def __init__(self, project: Project, parent=None):
        super().__init__(parent) # Call the inherited classes __init__ method
        uic.loadUi(resourcePath("src/editor/activetab.ui"), self) # Load the .ui file
        self._project = project
        self.treeWidget.itemClicked.connect(self.itemClicked)
        self._layout = None
        self._project.addCompRenameCallBack(self.update)


    def initTable(self, layout):
        self.treeWidget.clear()
        lo = layout.getLayout().getLOComp()
        lo.reverse() # costly
        for comp in lo:
            ActiveCompItem(self._project, comp, self.treeWidget)
            #self.treeWidget.setItemWidget(item, 1, item.getChkBox())
        self._layout = layout


    def update(self, old="", new=""):
        self.treeWidget.clear()
        self.initTable(self._layout)


    def clearTable(self):
        self.treeWidget.clear()


    def resizeEvent(self, evt) -> None:
        """
        Anytime the treeview is resized, this is called to have
        each column to be sized proportionately. 

        :param evt: resize event information
        :return: none
        """
        width = self.treeWidget.width() // self.treeWidget.columnCount()

        self.treeWidget.header().resizeSection(0, width)

        
    def itemClicked(self, item: ActiveCompItem, column: int) -> None:
        """
        When an item is clicked, this function is called to update the
        properties table.
        """
        if type(item) is ActiveCompItem:
            item.clicked()
