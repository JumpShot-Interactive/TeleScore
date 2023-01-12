"""
Developed by: JumpShot Team
Written by: riscyseven
"""

from attr import PropInstType, CompAttr, CompList, CompType
from component.basiccomp.clocksetcomp import ClockSetComp
from component.basiccomp.buttoncomp import ButtonComp
from component.basiccomp.clockcomp import ClockComp
from component.basiccomp.pointscomp import PointsComp
from component.basiccomp.defaultcomp import DefaultComp
from component.basiccomp.scoresetcomp import ScoreSetComp
from component.basiccomp.pointscomp import PointsComp
from component.teamcomp.teamcomp import TeamComp
from component.basiccomp.scorenumcomp import ScoreNumComp
from component.penalty.penaltycomp import PenaltyComp
from component.basiccomp.textsetcomp import TextSetComp
from component.basiccomp.textcomp import TextComp
from component.basiccomp.imagecomp import ImageComp
from component.basiccomp.imagesetcomp import ImageSetComp



class CompFactory:
    """
    Factory design patttern used to create category tabs in the component list.
    """

    factory = {
            "Time Display": [ClockComp],
            "Type Time Amount": [ClockSetComp],
            "Points Display": [PointsComp],
            "Add Points": [ScoreSetComp, ScoreSetComp.INC],
            "Sub Points": [ScoreSetComp, ScoreSetComp.DEC],
            "Points Set": [ScoreSetComp, ScoreSetComp.SET],
            "Team Attribute": [TeamComp],
            "Type Points Amount": [ScoreNumComp],
            "Penalty": [PenaltyComp],
            "Text Display": [TextComp],
            "Type Text": [TextSetComp],
            "Image Display": [ImageComp],
            "Image Set": [ImageSetComp]}

    @classmethod
    def makeComponent(self, project, compName: str, objectName, parent=None):
        allCompList = CompList.getAllCategory()

        comp = DefaultComp(project, objectName, parent)
        if (compName not in allCompList):
            return comp

        if (allCompList[compName][PropInstType.TYPE] == CompType.BUTTON):
            item = allCompList[compName]
            comp = ButtonComp(project, compName, item[CompAttr.TEXT], item[CompAttr.SIGNAL], objectName, parent)
            comp.setButtonColor(item[CompAttr.COLOR])

        
        if compName in self.factory:
            if len(self.factory[compName]) == 1:
                comp = self.factory[compName][0](project, objectName, parent)
            else:
                comp = self.factory[compName][0](project, objectName, self.factory[compName][1], parent)

        return comp
