"""
Developed By: JumpShot Team
Written by: riscyseven
"""

from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QUndoCommand

from project import Project
from layout.ctrllayout import CtrlLayout
from component.compfactory import CompFactory
from abstract.layoutcomp import LayoutComp
from attr import CompType

class InsertCmd(QUndoCommand):
    """
    Command used when insertting a component
    to the layout
    """

    def __init__(self, project: Project, layout: CtrlLayout, type: str, pos: QPoint, insertCallback, parent=None):
        """
        :param layout: Layout
        :param type: Component type (Ex. Clock)
        :param pos: Position of the component
        :param name: Object name
        """
        super().__init__(parent)
        self.layout = layout
        self._project = project
        self.type = type
        self.pos = pos
        self.component = None
        self._insertCallBack = insertCallback


    # Override
    def redo(self) -> None:
        """
        Insert command is executed and 
        component gets insertted to the layout

        :param: none
        :return: none
        """

        name = f"{self.type}{self._project.incCompCounter()}"
        while (self._project.existsComp(name)):
            name = f"{self.type}{self._project.incCompCounter()}"

        self.component = CompFactory.makeComponent(self._project, self.type,
         name, self.layout)

        if (self.component != None):
            self.component.move(self.pos)
            self.layout.addComponent(self.component)
            if (self.component.getType() == CompType.DISPLAY):
                self.component.setFileDir(self._project.getDefaultFileDir())
            self.component.setVisible(True)

        self._insertCallBack(self.component)


    # Override
    def undo(self) -> None:
        self.layout.removeComponent(self.component)


    def getComp(self) -> LayoutComp:
        """
        Returns the component this command is insertting.

        :param: none
        :return: Component
        """
        return self.component