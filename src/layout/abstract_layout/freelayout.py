"""
Developed By: JumpShot Team
Written by: riscyseven
"""

# This Python file uses the following encoding: utf-8
from PyQt6.QtWidgets import QGraphicsScene
from PyQt6.QtCore import QSize

class FreeLayout(QGraphicsScene):
    """
    New QLayout subclass that enables the component/widgets
    to be placed any where in the layout without any restrictions.
    """

    def __init__(self, size: QSize, parent=None):
        super().__init__(parent)
        self.size = size

