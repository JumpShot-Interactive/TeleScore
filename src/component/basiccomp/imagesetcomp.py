"""
Developed by: JumpShot Team
Written by: riscyseven
"""

from PyQt6.QtWidgets import QFileDialog

from component.basiccomp.buttoncomp import ButtonComp

class ImageSetComp(ButtonComp):
    def __init__(self, project, objectName, parent=None):
        super().__init__(project, "", "Set Image", "Set Image", objectName, parent)
        self.setButtonColor("#00A8E0")


    # Override
    def _onClick(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialog.setNameFilter("Image Files (*.png *.jpg *.bmp)")
        dialog.setViewMode(QFileDialog.ViewMode.Detail)
        if (dialog.exec() == dialog.DialogCode.Accepted):
            self._connection.emitSignal(self.signal, dialog.selectedFiles()[0])


    # Override
    def getName(self) -> str:
        return "Image Set"

