"""
Developed By: JumpShot Team
Written by: riscyseven
"""

from PyQt6.QtWidgets import QTreeWidgetItem
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from component.tabcomp import TabComp

class ActiveLOItem(QTreeWidgetItem):
    """
    Header item for the category list
    """

    def __init__(self, project, LO: TabComp, parent=None):
        super().__init__(parent)
        self.setText(0, LO.objectName())
        self.setFont(0, QFont("Segoe UI", 13))
        self.setTextAlignment(0, Qt.AlignmentFlag.AlignCenter)
