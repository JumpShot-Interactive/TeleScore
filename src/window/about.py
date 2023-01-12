"""
Developed By: JumpShot Team
Written by: riscyseven
"""

from PyQt6.QtWidgets import QDialog
from PyQt6 import uic

from gm_resources import resourcePath

class About(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._initUI()

    def _initUI(self):
        uic.loadUi(resourcePath("src/window/ui/about.ui"), self) # Load the .ui file