from queue import Queue

from editor.command.editpropcmd import EditPropCmd
from interface.propertiesinterface import PropertyInterface
from property.property.property import Property

class PropertyQueueUI:
    def __init__(self, cmdStack) -> None:
        self._queue = Queue()
        self._interface: PropertyInterface = None
        self._cmdStack = cmdStack


    def setInterface(self, interface: PropertyInterface):
        self._interface = interface


    def append(self, oldProp: Property, newProp: Property):
        self._queue.put((oldProp, newProp))
        self.flush() # TODO: remove this line


    def flush(self):
        while (not self._queue.empty()):
            oldProp, newProp = self._queue.get()
            cmd = EditPropCmd(self._interface, oldProp, newProp)
            self._cmdStack.push(cmd)