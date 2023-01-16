"""
Developed by: JumpShot Team
Written by: riscyseven
"""

from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtCore import Qt

from attr import CompPropTemplate
from abstract.displaycomp import DisplayComp
from fileio.fileout import ImageOut

from attr import CompPropTemplate, PropInstType, PropWidgetType

class ImageComp(DisplayComp):
    """
    Image component for scoreboard.
    """

    imageProp = {
        "Default Image": {
            PropInstType.TYPE: PropWidgetType.FLOPEN,
            PropInstType.VALUE: ""
        },
        "Transparent Background": {
            PropInstType.TYPE: PropWidgetType.CHECKBOX,
            PropInstType.VALUE: False
        }
    }

    def __init__(self, project, objectName, parent=None):
        super().__init__(project, objectName, "src/component/basiccomp/imagecomp.ui", parent)

        self.fileOut = ImageOut(self._properties["File Output Location"], parent=self)
        self._connection.appendCallBack("Set Image", self._setImage)
        self.label.setStyleSheet("background-color:#242325;")
        self.img = None


    # Override
    def _firstTimeProp(self):
        self._properties.appendPropHead("File Properties", CompPropTemplate.fileProperty)
        self._properties.appendPropHead("Image Properties", ImageComp.imageProp)


    # Override
    def getName(self) -> str:
        return "Image Display"


    # Override
    def _reloadProperty(self) -> None:
        self._properties["File Output Location"] = self.fileOut.getOutputFile()


    # Override 
    def _reconfProperty(self) -> None:
        if (self._properties["Enable File Output"]):
            if (self.fileOut.getOutputFile() != self._properties["File Output Location"]):
                self.fileOut.setOutputFile(self._properties["File Output Location"])
        
        self._setImage(self._properties["Default Image"])

        if (self._properties["Transparent Background"]):
            self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
            self.label.setStyleSheet("background-color:transparent;")
        else:
            self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
            self.label.setStyleSheet("background-color:#242325;")


    # Override
    def setFileDir(self, dirName):
        if (self._properties["Enable File Output"]):
            self._properties["File Output Location"] = dirName.format(self.objectName())
            self.fileOut.setOutputFile(self._properties["File Output Location"])


    def _clearImg(self):
        self.label.setVisible(True)
        self.img = None


    def _setImage(self, image):
        if (len(image) > 0):
            self.label.setVisible(False)
            self.img = QPixmap(image)
            if (self._properties["Enable File Output"]):
                self.fileOut.outputFile(self.img)
        else:
            self._clearImg()


    def paintEvent(self, a0) -> None:
        if self.img is not None:
            painter = QPainter(self)
            img = self.img.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            painter.drawPixmap(0, 0, img)
            painter.end()

        super().paintEvent(a0)


