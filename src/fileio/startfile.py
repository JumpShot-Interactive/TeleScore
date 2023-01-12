from json import load, dump, JSONDecodeError

from progsetting import ProgSetting
from project import Project

from abstract.abstractfile import AbstractFile

class StartFile(AbstractFile):
    def __init__(self):
        super().__init__()

    # Override
    def save(self):
        """
        Save the settings to a file.
        """
        jsonDict = {}
        fileDict = []

        setting = ProgSetting()

        for project in setting.getRecentlyOpened().values():
            fileDict.append(self.convProptoDict(project.getProperty().getAllPropDict()))
        jsonDict["1"] = fileDict
    
        try:
            with open(setting.getRUFileName(), "w") as f:
                dump(jsonDict, f)
        except FileNotFoundError:
            pass

    
    # Override
    def load(self):
        """
        Load the settings from a file.
        """
        jsonDict = {}
        setting = ProgSetting()

        try:
            with open(setting.getRUFileName(), "r") as f:
                jsonDict = load(f)

            for project in jsonDict["1"]:
                tempProj = Project()
                self.convDicttoProp(project, tempProj.getProperty())
                setting.addRecentlyOpened(tempProj)
        except (FileNotFoundError, JSONDecodeError) as e:
            print(e)
