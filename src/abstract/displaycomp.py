"""
Developed By: JumpShot Team
Written by: riscyseven
"""

from abstract.layoutcomp import LayoutComp
from abc import abstractmethod
from attr import CompType

class DisplayComp(LayoutComp):
    """
    DisplayComp is the base class for all components that
    displays information.

    DisplayComp is a subclass of LayoutComp
    """

    def __init__(self, project, objectName, uiFile, ctrlLayout):
        super().__init__(project, objectName, CompType.DISPLAY, uiFile, ctrlLayout)


    @abstractmethod
    def setFileDir(self, dirName):
        pass