"""
Developed By: JumpShot Team
Written by: riscyseven
"""

import os, sys
from PyQt6.QtGui import QUndoCommand

PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if PATH not in sys.path:
    sys.path.append(PATH)

class DeleteCmd(QUndoCommand):
    """
    Command used when insertting a component
    to the layout
    """

    def __init__(self, component, layout, parent=None):
        """
        :param layout: Layout
        :param type: Component type (Ex. Clock)
        :param pos: Position of the component
        :param name: Object name
        """
        super().__init__(parent)
        

    # Override
    def redo(self) -> None:
        pass

    # Override
    def undo(self) -> None:
        pass