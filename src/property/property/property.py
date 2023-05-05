"""
Developed by: JumpShot Team
Written by: riscyseven
"""

class Property:
    """
    This class is used to store the property of a component. 
    """

    def __init__(self, name=None, type=None, value=None, option=None, getCallback=None, setCallback=None):
        self._value = value
        self._type = type
        self._option = option
        self._name = name
        self._getCallback = getCallback
        self._setCallback = setCallback


    def setName(self, name):
        self._name = name

    
    def setType(self, type):
        self._type = type


    def setValue(self, value):
        self._value = value

    
    def setOption(self, option):
        self._option = option


    def getName(self):
        return self._name


    def getValue(self):
        return self._value

    
    def getType(self):
        return self._type


    def getOption(self):
        return self._option


    