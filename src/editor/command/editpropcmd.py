"""
Developed By: JumpShot Team
Written by: riscyseven
"""

from PyQt6.QtGui import QUndoCommand

class EditPropCmd(QUndoCommand):
    def __init__(self, properties, oldProp: list, newProp: list, parent=None):
        super().__init__(parent)
        self._oldProp = oldProp
        self._newProp = newProp
        self._properties = properties


    def redo(self):
        for prop in self._newProp:
            self._properties.setPropInst(prop.getName(), prop)
            if (prop.getUpdateMethod() != None):
                prop.getUpdateMethod()(prop.getValue())


    def undo(self):
        for prop in self._oldProp:
            self._properties.setPropInst(prop.getName(), prop)
            if (prop.getUpdateMethod() != None):
                prop.getUpdateMethod()(prop.getValue())