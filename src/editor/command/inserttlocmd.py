"""
Developed By: JumpShot Team
Written by: riscyseven
"""

from PyQt6.QtWidgets import QTabWidget
from PyQt6.QtGui import QUndoCommand

from component.tabcomp import TabComp

class InsertLOCmd(QUndoCommand):
    """
    Command used when insertting a component
    to the layout
    """

    def __init__(self, project, tabWidget: QTabWidget, editorInterface):
        """
        :param layout: Layout
        :param type: Component type (Ex. Clock)
        :param pos: Position of the component
        :param name: Object name
        """
        super().__init__()
        self.tabWidget = tabWidget
        self._editorInterface = editorInterface
        self.project = project
        self.tab = None


    # Override
    def redo(self) -> None:
        """
        Insert command is executed and 
        component gets insertted to the layout

        :param: none
        :return: none
        """
        name = f"Layout {self.project.incLOCounter()}"

        while (self.project.existsLO(name)):
            name = f"Layout {self.project.incLOCounter()}"
        
        self.tab = TabComp(self.project, name, self._editorInterface, self.tabWidget)
        self.tabWidget.addTab(self.tab, name)
        self.project.addLO(name, self.tab)


    # Override
    def undo(self) -> None:
        """
        
        """
        
        

    def getLayout(self) -> TabComp:
        return self.tab