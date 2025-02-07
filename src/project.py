from property.property import Property
from attr import CompType
from datetime import datetime
from attr import PropInstType, PropWidgetType
from os import getlogin, path, mkdir

class Project:
    """
    This class contains the project data.
    """

    projTemplate = {
        "Name": {
            PropInstType.TYPE: PropWidgetType.TEXTEDIT,
            PropInstType.VALUE: "untitled",
        },
        "Author": {
            PropInstType.TYPE: PropWidgetType.TEXTEDIT,
            PropInstType.VALUE: "TeleScore",
        },
        "Global Directory": {
            PropInstType.TYPE: PropWidgetType.DRSAVE,
            PropInstType.VALUE: "./Output/{}"
        }
    }

    projITemplate = {
        "CC": 0,
        "LC": 0,
    }

    def __init__(self, name: str="untitled", author: str="TeleScore"):
        self.property = Property()
        self.property.appendPropHead("Project", Project.projTemplate)
        self.property.appendProps(self.projITemplate)

        self.compDict = {}
        self.loDict = {}
        self.dirName = "./Output/{}"
        self.compCounter = 0
        self.loCounter = 0
        self._edit = False
        self._inEditor = False
        self.property["Date"] = ""
        self.property["FN"] = ""
        self.property["Author"] = getlogin()
        self.property["Version"] = "1.0.3 Beta Preview 1"
        self._renameLOCallBack = []
        self._renameCompCallBack = []


    def addLORenameCallBack(self, func):
        self._renameLOCallBack.append(func)


    def addCompRenameCallBack(self, func):
        self._renameCompCallBack.append(func)


    def setDate(self):
        self.property["Date"] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        
    
    def getProperty(self) -> Property:
        self.property["CC"] = self.compCounter
        self.property["LC"] = self.loCounter
        self.property["Global Directory"] = self.dirName.replace("/{}", "")
        return self.property

    
    def setProperty(self, prop: Property):
        self.property = prop
        self.compCounter = prop["CC"]
        self.loCounter = prop["LC"]
        self.dirName = prop["DIR"]


    def getProjectName(self) -> str:
        return self.property["Name"]


    def setFileName(self, fileName: str):
        self.property["FN"] = fileName


    def getFileName(self) -> str:
        return self.property["FN"]


    def addComp(self, name: str, comp) -> bool:
        if (not self.existsComp(name)):
            self.compDict[name] = comp
            return True
        return False


    def removeComp(self, comp):
        self.compDict.pop(comp.objectName())


    def removeCompByName(self, name: str):
        self.compDict.pop(name)


    def getComp(self, name: str):
        return self.compDict[name]


    def getAllComp(self):
        return self.compDict


    def existsComp(self, name: str) -> bool:
        return name in self.compDict


    def renameComp(self, oldName: str, newName: str):
        old = self.compDict[oldName]
        self.compDict[newName] = old

        del self.compDict[oldName]

        if (len(self._renameCompCallBack) > 0):
            for func in self._renameCompCallBack:
                func(oldName, newName)


    def incCompCounter(self) -> int:
        self.compCounter += 1
        return self.compCounter


    def getCompCount(self) -> int:
        return self.compCounter


    def addLO(self, name: str, LO) -> bool:
        if (not self.existsLO(name)):
            self.loDict[name] = LO
            return True
        return False


    def getLO(self, name: str):
        return self.loDict[name]


    def removeLO(self, LO):
        self.loDict.pop(LO.objectName())

    
    def removeLOByName(self, name: str):
        self.loDict.pop(name)


    def existsLO(self, name: str) -> bool:
        return name in self.loDict


    def renameLO(self, oldName: str, newName: str):
        old = self.loDict[oldName]
        self.loDict[newName] = old
        del self.loDict[oldName]
        if (len(self._renameLOCallBack) > 0):
            for func in self._renameLOCallBack:
                func(oldName, newName)


    def incLOCounter(self) -> int:
        self.loCounter += 1
        return self.loCounter


    def getLOCount(self) -> int:
        return self.loCounter


    def setDefaultFileDir(self, dirName):
        if (dirName[-1] == '/'):
            self.dirName = dirName + "{}"
        else:
            self.dirName = dirName + "/{}"

        if (not path.isdir(dirName.replace("{}", ""))):
            mkdir(dirName.replace("{}", ""))

        for comp in self.compDict.values():
            if (comp.getType() == CompType.DISPLAY):
                comp.setFileDir(self.dirName)


    def getAllLO(self):
        return self.loDict


    def getDefaultFileDir(self) -> str:
        return self.dirName


    def setEditMode(self, edit: bool):
        self._edit = edit


    def editMode(self) -> bool:
        return self._edit 


    def setInEditor(self, inEditor: bool):
        self._inEditor = inEditor


    def inEditor(self) -> bool:
        return self._inEditor


    def saveProperties(self):
        if (self.dirName.replace("/{}", "") != self.property["Global Directory"]):
            self.setDefaultFileDir(self.property["Global Directory"])