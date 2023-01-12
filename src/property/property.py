"""
Developed by: JumpShot Team
Written by: riscyseven
"""

from property.propinst.propinst import PropInst

class Property:
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


    def appendPropHead(self, headName:str, prop:dict):
        """
        Add a property template that contains rendering information
        """
        self._dispProp[headName] = []
        for name, propinst in prop.items():
            if (name in self._allProp):
                continue
            inst = PropInst(name=name, combined=propinst)
            self._allProp[name] = inst
            self._dispProp[headName].append(inst)


    def appendProps(self, prop: dict):
        """
        Add a property template that doesn't contain rendering information
        """
        for name, value in prop.items():
            if (name in self._allProp):
                continue
            self._allProp[name] = PropInst(name=name, value=value)


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


    def setValue(self, key: str, value: object) -> None:
        if (key in self._allProp):
            self._allProp[key].setValue(value)
        else:
            self._allProp[key] = PropInst(name=key, value=value)


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


    def getAllPropDict(self) -> dict:
        """
        Returns a dictionary that contains each property name as key
        and the property value

        :param: None
        :return: Dictionary that contains all properties
        """
        return self._allProp


    def getPropertyDict(self) -> dict:
        """
        Returns a formatted dictionary that contains the property header, it's
        content, and the value of each property. This should be mostly used for
        the property tab. 

        :param: None
        :return: Dictionary that contains formatted properties
        """
        return self._dispProp
