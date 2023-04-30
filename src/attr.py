"""
Developed by: JumpShot Team
Written by: riscyseven
Designed by: Fisk31
"""

class CompType():
    """
    Enum for the type of component
    """
    LAYOUT = 0
    DISPLAY = 1
    CONTROL = 2
    BUTTON = 3 # Probably a bad idea to put this here but it works.
    CUSTBUTTON = 4 # Probably a bad idea to put this here but it works.

class PropInstType:
    TYPE = 0
    VALUE = 1
    OPTION = 2
    NAME = 3

class PropWidgetType:
    TEXTEDIT = 0
    FONTEDIT = 1
    NUMEDIT = 2
    CONNEDIT = 3
    FLOPEN = 4
    FLSAVE = 5
    COLORPICK = 6
    CHECKBOX = 7
    COMBOBOX = 8
    HOTEDIT = 9
    DRSAVE = 10
    TYPE = 11
    VALUE = 12

class CompAttr():
    TABNAME = 0
    COMPONENT = 1
    ICON = 2
    HELP = 3
    TEXT = 4
    COLOR = 5
    SIGNAL = 6
    PROPERTY = 7
    Property = 9
    GENPROP = 10
    CONN = 11


class ProjAttr():
    HEADER = 0
    LAYOUTS = 1
    COMPONENTS = 2

class CompList:
    """
    Component dictionary will have a format:
    {
        Component Type Name: {
            ICON: (REQUIRED) loc to icon file
            TYPE: (REQUIRED) type of a component -> Currently DISPLAY, BUTTON, CUSTBUTTON
            COLOR: (REQUIRED FOR TYPE BUTTON) Color of the button
            SIGNAL: (REQUIRED FOR TYPE BUTTON) Name of the transmit type name
            HELP: (OPTIONAL BUT RECOMM) Helpful tip of the component
            More can be added in the future
        }
    }
    """

    timeComponent = {
        "Time Display": {
            CompAttr.ICON: "src/resources/tdisp.png",
            CompAttr.TEXT: "Time Display",
            PropInstType.TYPE: CompType.DISPLAY,
            CompAttr.HELP: "Time display provides a way to create a timer or a stopwatch with desired specification.\
                            \nConnect this component with a button to start, stop, and reset the timer."
        },
        "Start Time": {
            CompAttr.ICON: "src/resources/startButton.png",
            CompAttr.TEXT: "Start",
            CompAttr.COLOR: "#439a86",
            PropInstType.TYPE: CompType.BUTTON,
            CompAttr.SIGNAL: "Start",
            CompAttr.HELP: "Button to start the clock."
        },
        "Stop Time": {
            CompAttr.ICON: "src/resources/stopButton.png",
            CompAttr.TEXT: "Stop",
            CompAttr.COLOR: "#e15554",
            PropInstType.TYPE: CompType.BUTTON,
            CompAttr.SIGNAL: "Stop",
            CompAttr.HELP: "Button to stop the clock."
        },
        "Reset": {
            CompAttr.ICON: "src/resources/rstButton.png",
            CompAttr.TEXT: "Reset",
            CompAttr.COLOR: "#4357ad",
            PropInstType.TYPE: CompType.BUTTON,
            CompAttr.SIGNAL: "Reset",
            CompAttr.HELP: "Button to reset the clock."
        },
        "Add Seconds": {
            CompAttr.ICON: "src/resources/addSec.png",
            CompAttr.TEXT: "Add [+]\nSeconds",
            CompAttr.COLOR: "#242325",
            PropInstType.TYPE: CompType.BUTTON,
            CompAttr.SIGNAL: "ADDS",
            CompAttr.HELP: "Button to add seconds to the clock."
        },
        "Subtract Seconds": {
            CompAttr.ICON: "src/resources/subSec.png",
            CompAttr.TEXT: "Subtract [-]\nSeconds",
            CompAttr.COLOR: "#242325",
            PropInstType.TYPE: CompType.BUTTON,
            CompAttr.SIGNAL: "SUBS",
            CompAttr.HELP: "Button to subtract seconds from the clock."
        },
        "Add Minutes": {
            CompAttr.ICON: "src/resources/addMin.png",
            CompAttr.TEXT: "Add [+]\nMinutes",
            CompAttr.COLOR: "#242325",
            PropInstType.TYPE: CompType.BUTTON,
            CompAttr.SIGNAL: "ADDM",
            CompAttr.HELP: "Button to add minutes to the clock."
        },
        "Subtract Minutes": {
            CompAttr.ICON: "src/resources/subMin.png",
            CompAttr.TEXT: "Subtract [-]\nMinutes",
            CompAttr.COLOR: "#242325",
            PropInstType.TYPE: CompType.BUTTON,
            CompAttr.SIGNAL: "SUBM",
            CompAttr.HELP: "Button to subtract minutes from the clock."
        },
        "Type Time Amount": {
            CompAttr.ICON: "src/resources/setTime.png",
            CompAttr.TEXT: "",
            PropInstType.TYPE: CompType.DISPLAY,
            CompAttr.HELP: "Type in the amount of time to add or subtract from the clock."
        }
    }

    scoreComponent = {
        "Points Display": {
            CompAttr.ICON: "src/resources/scoreDisplay.png",
            CompAttr.TEXT: "Points Display",
            PropInstType.TYPE: CompType.DISPLAY,
            CompAttr.HELP: "Points display provides a way to display the current score/period of the game.\
                            \nConnect this component with a button to add or subtract points from the current score."
        },
        "Add Points": {
            CompAttr.ICON: "src/resources/addPtButton.png",
            CompAttr.TEXT: "Add Points",
            PropInstType.TYPE: CompType.CUSTBUTTON,
            CompAttr.HELP: "Button to add points to the current score."
        },
        "Sub Points": {
            CompAttr.ICON: "src/resources/subPtButton.png",
            CompAttr.TEXT: "Sub Points",
            PropInstType.TYPE: CompType.CUSTBUTTON,
            CompAttr.HELP: "Button to subtract points from the current score."
        }, 
        "Points Set": {
            CompAttr.ICON: "src/resources/scoreSet.png",
            CompAttr.TEXT: "Points Set",
            PropInstType.TYPE: CompType.DISPLAY,
            CompAttr.HELP: "Button to set the current score to a desired value."
        },
        "Type Points Amount": {
            CompAttr.ICON: "src/resources/setScoreNum.png",
            CompAttr.TEXT: "Type Points Amount",
            PropInstType.TYPE: CompType.DISPLAY,
            CompAttr.HELP: "Type the desired amount of points to be added or subtracted."
        }
    }

    teamCompoonent = {
        "Team Attribute": {
            CompAttr.ICON: "src/resources/teamComp.png",
            CompAttr.TEXT: "Team Attribute",
            PropInstType.TYPE: CompType.DISPLAY,
            CompAttr.HELP: "Team attribute provides a way to display the current team's name and score."
        }
    }

    miscComponent = {
        "Penalty": {
            CompAttr.ICON: "src/resources/penaltyComp.png",
            CompAttr.TEXT: "Penalty",
            PropInstType.TYPE: CompType.DISPLAY,
            CompAttr.HELP: "Penalty provides a way to display the current penalty of the game."
        }
    }

    appearComponent = {
        "Text Display": {
            CompAttr.ICON: "src/resources/textSource.png",
            CompAttr.TEXT: "Text Display",
            PropInstType.TYPE: CompType.DISPLAY,
            CompAttr.HELP: "Text display provides a way to display text on the screen.\
                            \nConnect this component with \"Type Text\" to set the text to display."
        },
        "Type Text": {
            CompAttr.ICON: "src/resources/textSet.png",
            CompAttr.TEXT: "Type Text",
            PropInstType.TYPE: CompType.DISPLAY,
            CompAttr.HELP: "Type text provides a way to type text to display on the screen.\
                            \nConnect this component with \"Text Display\" to set the text to display."
        },
        "Image Display": {
            CompAttr.ICON: "src/resources/imageSource.png",
            CompAttr.TEXT: "Image Display",
            PropInstType.TYPE: CompType.DISPLAY,
            CompAttr.HELP: "Image display provides a way to display an image on the screen.\
                            \nConnect this component with \"Image Set\" to set the image to display."
        },
        "Image Set": {
            CompAttr.ICON: "src/resources/imageSet.png",
            CompAttr.TEXT: "Image Set",
            PropInstType.TYPE: CompType.CUSTBUTTON,
            CompAttr.HELP: "Image set provides a way to set an image to display on the screen.\
                            \nConnect this component with \"Image Display\" to set the image to display."
        },
        "Visible": {
            CompAttr.ICON: "src/resources/setVisi.png",
            CompAttr.TEXT: "Visible",
            PropInstType.TYPE: CompType.BUTTON,
            CompAttr.COLOR: "#242325",
            CompAttr.SIGNAL: "Set Visible",
            CompAttr.HELP: "Connect this button to a component to make it visible"
        },
        "Invisible": {
            CompAttr.ICON: "src/resources/setInvisi.png",
            CompAttr.TEXT: "Invisible",
            PropInstType.TYPE: CompType.BUTTON,
            CompAttr.COLOR: "#242325",
            CompAttr.SIGNAL: "Set Invisible",
            CompAttr.HELP: "Connect this button to a component to make it invisible"
        }
    }

    category = [
            {
                CompAttr.TABNAME: "Time Based Buttons",
                CompAttr.COMPONENT: timeComponent
            },
            {
                CompAttr.TABNAME: "Points and Stats",
                CompAttr.COMPONENT: scoreComponent
            },
            {
                CompAttr.TABNAME: "Team Component",
                CompAttr.COMPONENT: teamCompoonent
            },
            {
                CompAttr.TABNAME: "Appearance Component",
                CompAttr.COMPONENT: appearComponent
            },
            {
                CompAttr.TABNAME: "Misc",
                CompAttr.COMPONENT: miscComponent
            }
        ]


    @classmethod
    def getAllCategory(self):
        # terrible code replace this in memory
        largeDict = {}
        for i in self.category:
            dict = i[CompAttr.COMPONENT]
            largeDict.update(dict)
        return largeDict


class CompPropTemplate:
    genProperty = {
        "Component Name": {
            PropInstType.TYPE: PropWidgetType.TEXTEDIT,
            PropInstType.VALUE: ""
        },
    }

    appearProperty = {
        "Display Text": {
            PropInstType.TYPE: PropWidgetType.TEXTEDIT,
            PropInstType.VALUE: ""
        },
        "Display Font": {
            PropInstType.TYPE: PropWidgetType.FONTEDIT,
            PropInstType.VALUE: ""
        },
        "Text Alignment": {
            PropInstType.TYPE: PropWidgetType.COMBOBOX,
            PropInstType.VALUE: 1,
            PropInstType.OPTION: ["Left", "Center", "Right"]
        },
        "Font Size": {
            PropInstType.TYPE: PropWidgetType.NUMEDIT,
            PropInstType.VALUE: 10
        },
        "Auto Font Size": {
            PropInstType.TYPE: PropWidgetType.CHECKBOX,
            PropInstType.VALUE: False
        },
        "Font Color": {
            PropInstType.TYPE: PropWidgetType.COLORPICK,
            PropInstType.VALUE: "#000000"
        },
        "Font Weight": {
            PropInstType.TYPE: PropWidgetType.COMBOBOX,
            PropInstType.VALUE: 0,
            PropInstType.OPTION: ["300", "400", "500", "600", "700", "800", "900"]
        },
        "Background Color": {
            PropInstType.TYPE: PropWidgetType.COLORPICK,
            PropInstType.VALUE: "#FFFFFF"
        },
        "Transparent Background": {
            PropInstType.TYPE: PropWidgetType.CHECKBOX,
            PropInstType.VALUE: False
        }
    }

    connProperty = {
        "Connection": {
            PropInstType.TYPE: PropWidgetType.CONNEDIT,
            PropInstType.VALUE: []
        }
    }

    fileProperty = {
        "Enable File Output": {
            PropInstType.TYPE: PropWidgetType.CHECKBOX,
            PropInstType.VALUE: True
        },
        "File Output Location": {
            PropInstType.TYPE: PropWidgetType.FLSAVE,
            PropInstType.VALUE: "./Output/{}"
        },
    }

    hotkeyProperty = {
        "Hotkey": {
            PropInstType.TYPE: PropWidgetType.HOTEDIT,
            PropInstType.VALUE: ""
        }
    }


class SettingAttr:
    genProperty = {
        "Language": {
            PropInstType.TYPE: PropWidgetType.COMBOBOX,
            PropInstType.VALUE: 0,
            PropInstType.OPTION: ["English"]
        },
        "Always On Top": {
            PropInstType.TYPE: PropWidgetType.CHECKBOX,
            PropInstType.VALUE: False
        },
        "Oilers Mode": {
            PropInstType.TYPE: PropWidgetType.CHECKBOX,
            PropInstType.VALUE: False
        }
    }

    loProperty = {
        "Default Width": {
            PropInstType.TYPE: PropWidgetType.NUMEDIT,
            PropInstType.VALUE: 1280
        },
        "Default Height": {
            PropInstType.TYPE: PropWidgetType.NUMEDIT,
            PropInstType.VALUE: 720
        },
    }

    udProperty = {
        "Check for Updates": {
            PropInstType.TYPE: PropWidgetType.CHECKBOX,
            PropInstType.VALUE: False
        },
    }

class StartMenuAttr:
    NAME = 0
    ICON = 1
    FILE = 2

    templateList = {
        "New Project": {
            NAME: "New Project",
            ICON: "src/resources/blank.png"
        },
        "General Template": {
            NAME: "General Template",
            ICON: "src/resources/scoreboard.png",
            FILE: "src/resources/premade.json"
        }
    }