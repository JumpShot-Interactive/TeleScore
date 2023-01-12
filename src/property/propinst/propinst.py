from attr import PropInstType

class PropInst:
    """
    This class is used to store the property of a component. 
    """

    def __init__(self, name=None, type=None, value=None, option=None, combined=None):
        self._value = value
        self._type = type
        self._option = option
        if (combined is not None):
            if (PropInstType.OPTION in combined):
                self._option = combined[PropInstType.OPTION]
            if (PropInstType.NAME in combined):
                self._name = combined[PropInstType.NAME]
            self._type = combined[PropInstType.TYPE]
            self._value = combined[PropInstType.VALUE]
        self._name = name


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
