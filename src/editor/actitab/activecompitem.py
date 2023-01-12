"""
Developed By: JumpShot Team
Written by: riscyseven
"""

from PyQt6.QtWidgets import QTreeWidgetItem
from PyQt6.QtGui import QFont, QMouseEvent
from PyQt6.QtCore import Qt, QPointF

from abstract.layoutcomp import LayoutComp
from project import Project

class ActiveCompItem(QTreeWidgetItem):
    def __init__(self, project: Project, comp: LayoutComp, parent):
        super().__init__(parent) # This sets this component to be the subcomponent of the header
        self.role = Qt.ItemDataRole.DisplayRole; # All the items are for displaying
        self.setText(0, comp.objectName())
        self.setTextAlignment(0, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        self.setFont(0, QFont("Segoe UI", 11))
        '''self._chkBox = QCheckBox()

        self._chkBox.setChecked(comp.isVisible())

        self._chkBox.stateChanged.connect(self._checkBoxChanged)'''
        self._comp = comp


    def getChkBox(self):
        return self._chkBox


    def _checkBoxChanged(self, state):
        self._comp.setVisible(state)


    def clicked(self):
        self._comp.mousePressEvent(QMouseEvent(QMouseEvent.Type.MouseButtonPress, QPointF(0, 0), Qt.MouseButton.LeftButton, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier))
        self._comp.mouseReleaseEvent(QMouseEvent(QMouseEvent.Type.MouseButtonRelease, QPointF(0, 0), Qt.MouseButton.LeftButton, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier))