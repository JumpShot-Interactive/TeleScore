"""
Developed By: JumpShot Team
Written by: riscyseven
"""

from abstract.layoutcomp import LayoutComp
from attr import CompType
from abc import abstractmethod

class ControlComp(LayoutComp):
    """
    ControlComp is the base class for all components that
    controls the display components.

    ControlComp is a subclass of AbstractComp
    """

    def __init__(self, project, objectName, uiFile, ctrlLayout):
        super().__init__(project, objectName, CompType.CONTROL, uiFile, ctrlLayout)

    
    @abstractmethod
    def setEditorMode(self, mode):
        """
        This method is called when the editor mode is changed.
        """
        pass