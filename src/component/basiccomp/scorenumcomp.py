"""
Developed by: JumpShot Team
Written by: riscyseven
UI designed by: Fisk31
"""

from abstract.controlcomp import ControlComp

class ScoreNumComp(ControlComp):
    """
    CLock widget for scoreboard.

    This class has one clock object from the backend.
    """

    def __init__(self, project, objectName, parent=None):
        super().__init__(project, objectName, "src/component/basiccomp/scorenumcomp.ui", parent)

        if (project.editMode() == True):
            self.lineEdit.installEventFilter(self)
            self.pushButton.installEventFilter(self)

        self.pushButton.pressed.connect(self._pressed)
        self.lineEdit.returnPressed.connect(self._pressed)

    # Override
    def _firstTimeProp(self) -> None:
        self._connection.appendConnType("Set Points")


    # Override
    def _reloadProperty(self) -> None:
        pass


    # Override
    def getName(self) -> str:
        return "Type Points Amount"


    # Override
    def _reconfProperty(self) -> None:
        pass


    # Override
    def setEditorMode(self, mode):
        pass


    def _pressed(self):
        number = self.lineEdit.text()
        try:
            number = int(number)
        except ValueError:
            number = 0
        self._connection.emitSignal("Set Points", number)