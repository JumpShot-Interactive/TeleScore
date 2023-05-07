from abc import abstractmethod

from property.properties import Properties

class AbstractFile:
    def __init__(self) -> None:
        pass

    def convProptoDict(self, prop) -> dict:
        tempProp = {}
        for name, propInst in prop.items():
            tempProp[name] = propInst.getValue()

        return tempProp


    def convDicttoProp(self, dict: dict, property: Properties):
        for key, value in dict.items():
            property[key] = value


    @abstractmethod
    def save(self):
        pass


    @abstractmethod
    def load(self):
        pass