"""
Developed by: JumpShot Team
Written by: riscyseven
Designed by: Fisk31
"""

from abstract.displaycomp import DisplayComp

class DefaultComp(DisplayComp):
    """
    You found me, easteregg
    """

    def __init__(self, project, objectName, parent=None):
        super().__init__(project, objectName, "src/component/basiccomp/defaultcomp.ui", parent)

    # Override
    def _firstTimeProp(self) -> None:
        pass

    # Override
    def getName(self) -> str:
        return ""

    # Override
    def _reloadProperty(self) -> None:
        pass

    # Override
    def _reconfProperty(self) -> None:
        pass

    # Override
    def setFileDir(self, dirName):
        pass