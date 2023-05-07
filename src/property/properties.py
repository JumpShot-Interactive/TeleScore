"""
Developed by: JumpShot Team
Written by: riscyseven
"""

from property.property.property import Property
from attr import PropInstType

class Properties:
    """
    This class is used to store the properties.
    """

    def __init__(self):
        self._dispProp = {}
        self._allProp = {}


    def __getitem__(self, key):
        return self.getValue(key)


    def __setitem__(self, key, value):
        self.setValue(key, value)


    def appendPropHead(self, headName: str, protoProp: dict):
        """
        Add a property template that contains rendering information
        """
        self._dispProp[headName] = []
        for name, protoPropInst in protoProp.items():
            if (name in self._allProp):
                continue
            inst = Property(name=name)
            self.trySettingAllProp(protoPropInst, inst)
            self._allProp[name] = inst
            self._dispProp[headName].append(inst)

    
    def trySettingAllProp(self, protoProp: dict, prop: Property):
        """
        Try to set all the properties in the dictionary
        """
        attributeDict = {
            PropInstType.TYPE: Property.setType,
            PropInstType.VALUE: Property.setValue,
            PropInstType.OPTION: Property.setOption,
            PropInstType.GET_CALLBACK: Property.setGetMethod,
            PropInstType.UPDATE_CALLBACK: Property.setUpdateMethod
        }

        for attr, value in protoProp.items():
            if (attr in attributeDict):
                attributeDict[attr](prop, value)


    def appendProps(self, prop: dict):
        """
        Add a property template that doesn't contain rendering information
        """
        for name, value in prop.items():
            if (name in self._allProp):
                continue
            self._allProp[name] = Property(name=name, value=value)


    def removePropHead(self, headName: str):
        for i in self._dispProp[headName].getName():
            self._allProp.pop(i)
        self._dispProp.pop(headName)


    def removeProp(self, name: str):
        inst = self._allProp.pop(name)
        for head in self._dispProp.values():
            if (inst in head):
                head.remove(inst)
                break


    def setValue(self, key: str, value: object):
        if (key in self._allProp):
            self._allProp[key].setValue(value)
        else:
            self._allProp[key] = Property(name=key, value=value)


    def setPropInst(self, key: str, prop: Property):
        self._allProp[key] = prop

        # TODO: This is a very inefficient way of doing this
        for head in self._dispProp.values():
            for inst in head:
                if (inst.getName() == key):
                    index = head.index(inst)
                    head[index] = prop
                    return


    def getPropInst(self, key: str) -> Property:
        if (key in self._allProp):
            return self._allProp[key]
        return None


    def getValue(self, attr) -> object:
        """
        Get the value of the property, this value can be any type of object
        NOTE: Developers can use "[]" instead

        :param attr: 
        """
        if (attr not in self._allProp):
            return None
        return self._allProp[attr].getValue()


    def getValueFromOption(self, attr: str):
        """
        Get the value of the property from the option, this value can be any type of object

        :param attr: 
        """
        if (attr not in self._allProp):
            return None
        return self._allProp[attr].getOption()[self._allProp[attr].getValue()]


    def getOption(self, attr) -> object:
        """
        Get the option of the property, this value can be any type of object
        NOTE: Developers can use "[]" instead

        :param attr: 
        """
        if (attr not in self._allProp):
            return None
        return self._allProp[attr].getOption()


    def getAllKeyValuePair(self) -> dict:
        """
        Returns a dictionary that contains each property name as key
        and the property value

        :param: None
        :return: Dictionary that contains all properties
        """
        return self._allProp


    def getCategorizedProperties(self) -> dict:
        """
        Returns a formatted dictionary that contains the property header, it's
        content, and the value of each property. This should be mostly used for
        the property tab. 

        :param: None
        :return: Dictionary that contains formatted properties
        """
        return self._dispProp