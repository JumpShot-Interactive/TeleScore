"""
Developed By: JumpShot Team
Written by: riscyseven
"""

from PyQt6.QtWidgets import QTabWidget
from PyQt6.QtGui import QUndoCommand

from component.tabcomp import TabComp

class DeleteLOCmd(QUndoCommand):
    """
    Command used when insertting a component
    to the layout
    """

    def __init__(self, project, index, tabWidget: QTabWidget):
        """
        :param layout: Layout
        :param type: Component type (Ex. Clock)
        :param pos: Position of the component
        :param name: Object name
        """
        super().__init__()
        self.tabWidget = tabWidget
        self.project = project
        self.index = index


    # Override
    def redo(self) -> None:
        widget = self.tabWidget.widget(self.index)
        self.tabWidget.removeTab(self.index)

        for comp in widget.getLayout().getLOComp():
            self.project.removeComp(comp)

        self.project.removeLO(widget)
        widget.setParent(None)
        widget.deleteLater()


    # Override
    def undo(self) -> None:
        """
        
        """
        

    def getLayout(self) -> TabComp:
        return self.tab