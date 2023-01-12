"""
Developed by: JumpShot Team
Written by: riscyseven
UI designed by: Fisk31
"""
from attr import PropInstType, PropWidgetType
from abstract.controlcomp import ControlComp

class ClockSetComp(ControlComp):
    """
    Clock set component for scoreboard.

    Manually type in time amount.
    """

    clockSetProp = {
        "Format": {
            PropInstType.TYPE: PropWidgetType.COMBOBOX,
            PropInstType.VALUE: 0,
            PropInstType.OPTION: ["mm:ss", "hh:mm:ss", "mm:ss.z", "hh:mm:ss.z"],
        },
        "Preset Time": {
            PropInstType.TYPE: PropWidgetType.TEXTEDIT,
            PropInstType.VALUE: "00:00"
        }
    }

    def __init__(self, project, objectName, parent=None):
        super().__init__(project, objectName, "src/component/basiccomp/clocksetcomp.ui", parent)

        if (project.inEditor()):
            self.lineEdit.installEventFilter(self)
            self.pushButton.installEventFilter(self)

        self.pushButton.pressed.connect(self.pressed)
        self.lineEdit.returnPressed.connect(self.pressed)


    # Override
    def _firstTimeProp(self) -> None:
        self._properties.appendPropHead("Clock Set Properties", self.clockSetProp)
        self._connection.appendConnType("Set Time")


    # Override
    def _reloadProperty(self) -> None:
        pass


    # Override
    def getName(self) -> str:
        return "Type Time Amount"


    # Override
    def _reconfProperty(self) -> None:
        text = self._cleanFormat(self._properties.getValueFromOption("Format"))
        self.lineEdit.setInputMask(text)
        self.lineEdit.setText(self._properties["Preset Time"])


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
        self._connection.emitSignal("Set Time", (self.lineEdit.text(),
         self._properties.getValueFromOption("Format")))


    def _cleanFormat(self, text):
        return text.replace("z", "0").replace("s", "0").replace("m", "0").replace("h", "0")