"""
Developed by: JumpShot Team
Written by: riscyseven
"""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QFileDialog

from attr import PropWidgetType, PropInstType, CompPropTemplate
from abstract.displaycomp import DisplayComp
from fileio.fileout import TextOut, ImageOut

class TeamComp(DisplayComp):
    """
    Temporary Team Component
    """

    imageProperty = {
        "Logo Width": {
            PropInstType.TYPE: PropWidgetType.NUMEDIT,
            PropInstType.VALUE: 80
        },
        "Logo Height": {
            PropInstType.TYPE: PropWidgetType.NUMEDIT,
            PropInstType.VALUE: 80
        }
    }
    
    def __init__(self, project, objectName,  parent=None):
        super().__init__(project, objectName, "src/component/teamcomp/teamcomp.ui", parent)

        self.fileName = self._properties["File Output Location"]
        self.logo = None
        self.verticalLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.icon_pushButton.clicked.connect(self._onLogoButton)
        self.setteam_PushButton.clicked.connect(self._setTeamButton)

        self.nameOut = TextOut(self._properties["File Output Location"] + "-name", self)
        self.attrOut = TextOut(self._properties["File Output Location"] + "-attr", self)
        self.logoOut = ImageOut(self._properties["File Output Location"] + "-logo", self)

        self._properties.removeProp("Enable File Output")


    # Override
    def _firstTimeProp(self):
        self._properties.appendPropHead("File Properties", CompPropTemplate.fileProperty)
        self._properties.appendPropHead("Logo Properties", self.imageProperty)

    # Override
    def _reloadProperty(self):
        self._properties["File Output Location"] = self.fileName

    # Override
    def _reconfProperty(self):
        if (self.fileName != self._properties["File Output Location"]):
            self.fileName = self._properties["File Output Location"]
            self.nameOut.setOutputFile(self._properties["File Output Location"] + "-name")
            self.attrOut.setOutputFile(self._properties["File Output Location"] + "-attr")
            self.logoOut.setOutputFile(self._properties["File Output Location"] + "-logo")
            self.attrChanged.emit()

    # Override
    def getName(self) -> str:
        return "Team Attribute"

    # Override
    def setFileDir(self, dirName):
        self._properties["File Output Location"] = dirName.format(self.objectName())
        self.fileName = self._properties["File Output Location"]
        self.nameOut.setOutputFile(self._properties["File Output Location"] + "-name")
        self.attrOut.setOutputFile(self._properties["File Output Location"] + "-attr")
        self.logoOut.setOutputFile(self._properties["File Output Location"] + "-logo")

    def _onLogoButton(self):
        fileName = QFileDialog.getOpenFileName(self, "Open Image Location", "", "Image File (*.png *.jpg)")[0]
        if (fileName != ""):
            pixmap = QPixmap(fileName)
            icon = QIcon(pixmap)
            self.icon_pushButton.setIcon(icon)
            self.icon_pushButton.setIconSize(self.icon_pushButton.size())
            self.icon_pushButton.setText("")

            self.logo = pixmap.scaled(self._properties["Logo Width"], self._properties["Logo Height"])

    def _setTeamButton(self):
        name = self.nameLineEdit.text()
        attr = self.attrLineEdit.text()
        self.nameOut.outputFile(name)
        self.attrOut.outputFile(attr)

        if (self.logo != None):
            self.logoOut.outputFile(self.logo)
        