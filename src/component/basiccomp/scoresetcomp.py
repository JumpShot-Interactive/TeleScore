"""
Developed by: JumpShot Team
Written by: riscyseven
UI designed by: Fisk31
"""

from attr import PropWidgetType, PropInstType
from component.basiccomp.buttoncomp import ButtonComp

class ScoreSetComp(ButtonComp):
    """
    Points Set Button

    Class defines the functionality for the button that 
    sets the score
    """

    SET = "Points Set"
    INC = "Add Points"
    DEC = "Sub Points"

    scoreSetProperty = {
        "Set Amount": {
            PropInstType.TYPE: PropWidgetType.NUMEDIT,
            PropInstType.VALUE: 0
        }
    }

    def __init__(self, project, objectName, delta=SET, parent=None):
        super().__init__(project, "", "", "", objectName,  parent) # Probably want to refract this

        self.setButtonColor("#863EA8")
        self._connection.removeConnType("")
        self.delta = delta
        self.value = 1
        self.hotKey = None
        match delta:
            case self.SET:
                self.pushButton.setText("Set\nNumber")
                self._connection.appendConnType("Set Points")
            case self.INC:
                self.pushButton.setText("Add [+]\nPoints")
                self.setButtonColor("#4357ad")
                self._connection.appendConnType("Add Points")
            case self.DEC:
                self.pushButton.setText("Sub [-]\nPoints")
                self.setButtonColor("#e15554")
                self._connection.appendConnType("Sub Points")


    # Override
    def _firstTimeProp(self):
        self._properties.appendPropHead("Set Properties", self.scoreSetProperty)
        super()._firstTimeProp()


    # Override
    def _reloadProperty(self) -> None:
        super()._reloadProperty()
        self._properties["Set Amount"] = self.value


    # Override
    def _reconfProperty(self) -> None:
        self.value = self._properties["Set Amount"]
        self.pushButton.setText(str(self.value))
        super()._reconfProperty()


    # Override
    def getName(self) -> str:
        return self.delta
 

    # Override
    def _onClick(self):
        match self.delta:
            case self.SET:
                self._connection.emitSignal("Set Points", self.value)
            case self.INC:
                self._connection.emitSignal("Add Points", self.value)
            case self.DEC:
                self._connection.emitSignal("Sub Points", self.value)