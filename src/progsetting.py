"""
Developed By: JumpShot Team
Written by: riscyseven
"""

from property.properties import Properties
from attr import SettingAttr
from fileio.settingfile import SettingFile
from os.path import exists

class ProgSetting(object):
    """
    This class is the singleton class that holds the program's settings.
    """
    properties = Properties()
    recentlyOpened = {}

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ProgSetting, cls).__new__(cls)
        return cls.instance
    

    def loadProperties(self, path: str):
        self.properties = Properties()
        self.properties.appendPropHead("General", SettingAttr.genProperty)
        try:
            settingFile = SettingFile(path, self.properties)
            settingFile.load()
        except FileNotFoundError:
            pass


    def saveProperties(self, path: str):
        settingFile = SettingFile(path, self.properties)
        settingFile.save()


    def getProperties(self) -> Properties:
        return self.properties


    def addRecentlyOpened(self, project):
        if (exists(project.getFileName())):
            if (project.getFileName() in self.recentlyOpened):
                self.recentlyOpened.pop(project.getFileName())
            self.recentlyOpened[project.getFileName()] = project
            if len(self.recentlyOpened) > 10:
                self.recentlyOpened.popitem()


    def getRecentlyOpened(self) -> dict:
        return self.recentlyOpened


    def setRecentlyOpened(self, projects: dict):
        self.recentlyOpened = projects

    
    def removeRecentlyOpened(self, fileName: str):
        self.recentlyOpened.pop(fileName)


    def getRUFileName(self) -> str:
        return "required/recentlyOpened.json"