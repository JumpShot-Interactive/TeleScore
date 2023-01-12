"""
Developed by: JumpShot Team
Written by: riscyseven
UI designed by: Fisk31
"""

from abstract.controlcomp import ControlComp

class TextSetComp(ControlComp):
    """
    Text set component for scoreboard.
    """

    def __init__(self, project, objectName, parent=None):
        super().__init__(project, objectName, "src/component/basiccomp/textsetcomp.ui", parent)

        if (project.inEditor()):
            self.lineEdit.installEventFilter(self)
            self.pushButton.installEventFilter(self)

        self.pushButton.pressed.connect(self.pressed)
        self.lineEdit.returnPressed.connect(self.pressed)


    # Override
    def _firstTimeProp(self) -> None:
        self._connection.appendConnType("Set Text")


    # Override
    def _reloadProperty(self) -> None:
        pass


    # Override
    def getName(self) -> str:
        return "Type Text"


    # Override
    def _reconfProperty(self) -> None:
        pass


    # Override
    def setFileDir(self, dirName):
        pass


    # Override
    def setEditorMode(self, mode):
        if (mode):
            self.lineEdit.installEventFilter(self)
            self.pushButton.installEventFilter(self)
        else:
            self.lineEdit.removeEventFilter(self)
            self.pushButton.removeEventFilter(self)


    def pressed(self):
        self._connection.emitSignal("Set Text", self.lineEdit.text())