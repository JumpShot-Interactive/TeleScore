from json import load, dump, JSONDecodeError
from abstract.abstractfile import AbstractFile


class SettingFile(AbstractFile):
    def __init__(self, fileName: str, property):
        self._fileName = fileName
        self._property = property


    # Override
    def save(self):
        """
        Save the settings to a file.
        """
        jsonDict = {}
        jsonDict["properties"] = self.convProptoDict(self._property.getAllPropDict())

        try: 
            with open(self._fileName, "w") as file:
                dump(jsonDict, file)
        except FileNotFoundError:
            pass


    # Override
    def load(self):
        """
        Load the settings from a file.
        """
        jsonDict = {}
        
        with open(self._fileName, "r") as file:
            try:
                jsonDict = load(file)
            except JSONDecodeError:
                return

        for key, value in jsonDict["properties"].items():
            self._property[key] = value