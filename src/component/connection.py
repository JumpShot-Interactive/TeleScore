"""
Developed by: JumpShot Team
Written by: riscyseven
"""

from copy import copy

class Connection:
    COMP = 0
    TYPE = 1
    EXTRA = 2

    HELLO_PKT = -1
    BYEA2B_PKT = -2
    BYEB2A_PKT = -3

    """
    A2Bconnection dictionary format:
        { 
            TypeName1: [component1, component2],
            TypeName2: [component3, component4]
        }

    A2Bcallback dictionary format:
        {
            TypeName1: callbackFunc
        }
    
    B2Aconnection dictionary format:
        {
            component1: TypeName
        }
    """

    def __init__(self, comp):
        self.A2Bconnection = {} # Contains the type of the connection and the list of components assigned
        self.A2Bcallback = {} # Contains callback when the appended connection type is received

        self.B2Aconnection = [] # Contains components (A2B) that are connected to this component
        self.selfComponent = comp

        self.aA2Bconnection = {}
        self.aB2Aconnection = {}


    def appendConnType(self, typeName):
        self.A2Bconnection[typeName] = []


    def appendConn(self, typeName, component):
        """
        
        """
        if (component not in self.A2Bconnection[typeName]):
            self.A2Bconnection[typeName].append(component)
            component.getConnection().handShake(self.HELLO_PKT, (self.selfComponent, typeName))


    def removeA2BConn(self, typeName, component):
        self.A2Bconnection[typeName].remove(component)
        component.getConnection().handShake(self.BYEA2B_PKT, (self.selfComponent, typeName))


    def removeB2AConn(self, typeName, component):
        """
        Remove specific incoming signal
        """
        component.getConnection().handShake(self.BYEB2A_PKT, (self.selfComponent, typeName))
        self.B2Aconnection.remove((component, typeName))


    def removeAllB2AConn(self):
        """
        Remove any incoming signals
        """
        for i in self.B2Aconnection:
            i[0].getConnection().handShake(self.BYEB2A_PKT, (self.selfComponent, i[1]))
        self.B2Aconnection = []


    def removeAllA2BConn(self):
        """
        Remove any outgoing signals
        """
        for i in self.A2Bconnection:
            for j in self.A2Bconnection[i]:
                j.getConnection().handShake(self.BYEA2B_PKT, (self.selfComponent, i))
            self.A2Bconnection[i] = []


    def removeAllConnection(self):
        self.removeAllA2BConn()
        self.removeAllB2AConn()
    
    
    def appendCallBack(self, name, callback):
        self.A2Bcallback[name] = callback


    def emitSignal(self, typeName, extra=None):
        list = self.A2Bconnection[typeName]
        for i in list:
            i.getConnection().received(typeName, extra)


    def handShake(self, typeName, extra):
        match typeName:
            case self.HELLO_PKT:
                self.B2Aconnection.append((extra[0], extra[1]))
            case self.BYEA2B_PKT:
                self.B2Aconnection.remove((extra[0], extra[1]))
            case self.BYEB2A_PKT:
                self.A2Bconnection[extra[1]].remove(extra[0])


    def received(self, typeName, extra):
        """
        This is called when a transmitting component emits a signal

        :param:
        """
        if (extra != None):
            self.A2Bcallback[typeName](extra)
        else:
            self.A2Bcallback[typeName]()


    def getData(self) -> tuple:
        """
        
        """
        self.aA2Bconnection = {}
        for type in self.A2Bconnection:
            self.aA2Bconnection[type] = copy(self.A2Bconnection[type])
        self.aB2Aconnection = copy(self.B2Aconnection)
        return (self.aA2Bconnection, self.aB2Aconnection)


    def dataChanged(self):
        for type in self.A2Bconnection:    # Usually going to be n=1
            for component in self.A2Bconnection[type]:
                if (component not in self.aA2Bconnection[type]):
                    self.removeA2BConn(type, component)

        # Add the new connections
        for type in self.A2Bconnection:
            for component in self.aA2Bconnection[type]:
                self.appendConn(type, component)

        for tuple in self.B2Aconnection:
            if (tuple not in self.aB2Aconnection):
                self.removeB2AConn(tuple[1], tuple[0])
    

    def removeConnType(self, typeName):
        del self.A2Bconnection[typeName]


    def getSignalTypes(self) -> list:
        types = []
        for i in self.A2Bconnection:
            types.append(i)
        return types


    def getRecvTypes(self) -> list:
        types = []
        for i in self.A2Bcallback:
            types.append(i)
        return types
