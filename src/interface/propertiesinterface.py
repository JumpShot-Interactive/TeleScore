from abc import ABC, abstractmethod

class PropertiesInterface(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def setPropQueue(self, prop):
        pass

    @abstractmethod
    def updateProp(self):
        pass