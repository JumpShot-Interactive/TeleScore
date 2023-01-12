"""
Developed By: JumpShot Team
Written by: riscyseven
"""

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QTreeWidgetItem
from PyQt6.QtCore import Qt

class PropWidgetHead(QTreeWidgetItem):
    """
    Header item for the category list
    """

    def __init__(self, text="Default", parent=None):
        super().__init__(parent)
        self.setText(0, text)
        self.setFont(0, QFont("Segoe UI", 13))
        self.setTextAlignment(0, Qt.AlignmentFlag.AlignCenter)