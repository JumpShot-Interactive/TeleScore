"""
Developed By: JumpShot Team
Written by: riscyseven
"""

from PyQt6.QtGui import QUndoCommand

class EditPropCmd(QUndoCommand):
    def __init__(self, properties, oldProp, newProp, parent=None):
        super().__init__(parent)
        self._oldProp = oldProp
        self._newProp = newProp
        self._properties = properties


    def redo(self):
        self._properties.setPropInst(self._newProp)


    def undo(self):
        self._properties.setPropInst(self._oldProp)