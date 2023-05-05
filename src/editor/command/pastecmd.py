from PyQt6.QtWidgets import QUndoCommand

class PasteCmd(QUndoCommand):
    def __init__(self, project, component, parent=None):
        super().__init__(parent)
        self._project = project
        self._component = component

    # Override
    def redo(self) -> None:
        self._project.addComp(self._component)
    

    # Override
    def undo(self) -> None:
        self._project.removeComp(self._component)