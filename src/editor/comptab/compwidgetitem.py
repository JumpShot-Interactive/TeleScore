"""
Developed By: JumpShot Team
Written by: riscyseven
"""

from PyQt6.QtWidgets import QPushButton, QTreeWidgetItem
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt, QSize

from gm_resources import GMessageBox, resourcePath

class CompWidgetItem(QTreeWidgetItem):
    """
    Each component listed in the component list is made from 
    this class object. This widget item will standardize attributes
    such as the fonts, icon image size, etc.
    """

    def __init__(self, icon: QIcon, text: str, info: str, parent, treeWidget):
        """
        Consturctor for a component list item

        :param icon: Icon for the component
        :param parent: Header/category of the item
        :param treeWidget: Main component list widget
        :param text: Description of the component

        :return: none
        """
        super().__init__(parent) # This sets this component to be the subcomponent of the header
        self.setText(0, text)
        self.setTextAlignment(0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.setFont(0, QFont("Segoe UI", 12))
        self.info = info
        if (icon != None):
            self.setIconFile(icon)

        self._infoButton = QPushButton(QIcon(resourcePath("src/resources/infoButton.png")), "", treeWidget)
        self._infoButton.setProperty("class", "InfoButton")
        self._infoButton.setStyleSheet("QPushButton{border: none;}")
        self._infoButton.pressed.connect(self._infoButtonClicked)
        self._infoButton.released.connect(self._infoButtonReleased)
        self._infoButton.setIconSize(QSize(20, 20))

        self._treeWidget = treeWidget


    def get_infoButton(self):
        return self._infoButton


    def _infoButtonReleased(self):
        self._infoButton.setIcon(QIcon(resourcePath("src/resources/infoButton.png")))


    def _infoButtonClicked(self):
        self._infoButton.setIcon(QIcon(resourcePath("src/resources/infoButtonDown.png")))
        msg = GMessageBox(f"Information about: {self.text(0)}", self.info, "Info", self._treeWidget)
        msg.exec()


    def setIconFile(self, iconFile: str) -> None:
        """
        Sets the icon next to the description

        :param iconFile: icon file location
        """
        icon = QIcon(iconFile)
        self.setIcon(0, icon)
        