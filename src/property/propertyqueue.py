from queue import Queue

from property.property.property import Property
from interface.propertiesinterface import PropertyInterface


class PropertyQueue:
    def __init__(self) -> None:
        self._queue = Queue()
        self._interface: PropertyInterface = None


    def setInterface(self, interface: PropertyInterface):
        self._interface = interface


    def append(self, prop: Property):
        self._queue.put(prop)


    def flush(self):
        while (not self._queue.empty()):
            prop = self._queue.get()
            self._properties.setPropInst(prop.getName(), prop)
