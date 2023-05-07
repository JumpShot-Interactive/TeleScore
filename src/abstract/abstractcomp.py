"""
Developed by: JumpShot Team
Written by: riscyseven
"""

from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import pyqtSignal
from abc import ABC, abstractmethod

from gm_resources import GMessageBox
from property.properties import Properties
from attr import CompPropTemplate, CompType, PropInstType
from project import Project

from copy import deepcopy

class Meta(type(ABC), type(QFrame)): pass

class AbstractComp(ABC, QFrame, metaclass=Meta):
    """
    Abstract class for components. 

    Contains implmentation requirements for a component, also contains functions that
    are required for the editor
    """

    compClicked = pyqtSignal(object) # Object should be AbstractComp
    attrChanged = pyqtSignal()

    def __init__(self, project: Project, objectName: str, type: CompType, parent=None):
        super().__init__(parent)
        self._properties = Properties()
        self._project = project
        self._type = type
        
        propInst = deepcopy(CompPropTemplate.genProperty)
        propInst["Component Name"][PropInstType.GET_CALLBACK] = self._getCompNameCallback
        propInst["Component Name"][PropInstType.UPDATE_CALLBACK] = self._setCompNameCallback

        self._properties.appendPropHead("General Properties", propInst)

        self.setObjectName(objectName)


    def getProperty(self) -> Properties:
        """
        Method that returns how the property tab should
        be setup for this instance of a button

        :param: none
        :return: property object
        """
        return self._properties


    def _getCompNameCallback(self) -> str:
        self._properties["Component Name"] = self.objectName()


    def _setCompNameCallback(self, newName: str):
        oldName = self.objectName()
        if (oldName != newName and len(newName) > 0):
            if (self._type == CompType.LAYOUT and
             not self._project.existsLO(newName)):
                self.setObjectName(newName)
                self._project.renameLO(oldName, newName)
            elif((self._type == CompType.DISPLAY or self._type == CompType.CONTROL) and
             not self._project.existsComp(newName)):
                self.setObjectName(newName)
                self._project.renameComp(oldName, newName)
            else:
                msgBox = GMessageBox("Cannot Change Component Name",
                 "This name is already taken by another component!", "Info", self)
                msgBox.exec()
                self._properties["Component Name"] = oldName
            self.attrChanged.emit()


    def getType(self) -> CompType:
        return self._type


    @abstractmethod
    def getName(self) -> str:
        """
        Return the _type of the component in str
        :param: none
        :return str: str that describes the component _type
        """
        pass


    @abstractmethod
    def _firstTimeProp(self):
        """
        When the component is initialized, this is called to make
        sure the subclasses insert correct _properties. This method will be
        called automatially by the this base class.

        :param: none
        :return: none
        """
        pass