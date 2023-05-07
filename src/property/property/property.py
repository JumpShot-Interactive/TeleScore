"""
Developed by: JumpShot Team
Written by: riscyseven
"""

class Property:
    """
    This class is used to store the property of a component. 
    """

    def __init__(self, name=None, type=None, value=None, option=None, updateMethod=None, getMethod=None):
        self._value = value
        self._type = type
        self._option = option
        self._name = name
        self._updateMethod = updateMethod
        self._getMethod = getMethod


    def copy(self, prop):
        self._value = prop.getValue()
        self._type = prop.getType()
        self._option = prop.getOption()
        self._name = prop.getName()
        self._updateMethod = prop.getUpdateMethod()
        self._getMethod = prop.getGetMethod()


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


    def setUpdateMethod(self, method):
        self._updateMethod = method

    
    def setGetMethod(self, method):
        self._getMethod = method


    def getUpdateMethod(self):
        """
        Returns the update method of the property.

        CHECK FOR NONE BEFORE CALLING THIS METHOD.
        """
        return self._updateMethod
    

    def getGetMethod(self):
        """
        Returns the get method of the property.

        CHECK FOR NONE BEFORE CALLING THIS METHOD.
        """
        return self._getMethod