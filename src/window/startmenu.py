"""
Developed By: JumpShot Team
Written by: riscyseven
"""

from PyQt6.QtWidgets import QWidget, QListWidgetItem, QTreeWidgetItem
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from gm_resources import resourcePath
from attr import StartMenuAttr
from progsetting import ProgSetting

class StartMenu(QWidget):
    def __init__(self, newCallBack, openCallBack, parent=None):
        super().__init__(parent) # Call the inherited classes __init__ method
        self.newCallBack = newCallBack
        self.openCallBack = openCallBack
        self.templateMap = {}
        self._initUI()


    def _initUI(self):
        """
        Initializes the startmenu UI.

        :param: none
        :return: none
        """
        path = resourcePath("src/window/ui/startmenu.ui")
        uic.loadUi(path, self) # Load the .ui file
        self.treeWidget.setProperty("class", "StartTreeWidget")
        self.treeWidget.header().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        self.listWidget.itemDoubleClicked.connect(self._newTemplateClicked)
        self.treeWidget.itemDoubleClicked.connect(self._openTemplateClicked)
        self._loadStartFile()
        self.treeWidget.topLevelItem(0).setTextAlignment(0, Qt.AlignmentFlag.AlignCenter)


    def _loadStartFile(self):
        """
        Loads the start file into the start menu

        :param: none
        :return: none
        """
        self.templateList = StartMenuAttr.templateList
        self._loadTemplates()
        self._loadRecent()


    def _newTemplateClicked(self, item: QListWidgetItem):
        if (item.text() == "New Project"):
            self.newCallBack()
        else:
            self.openCallBack(None, StartMenuAttr.templateList[item.text()][StartMenuAttr.FILE])


    def _openTemplateClicked(self, item: QTreeWidgetItem):
        self.openCallBack(None, item.text(3))


    def resizeEvent(self, evt):
        """
        Anytime the treeview is resized, this is called to have
        each column to be sized proportionately. 

        :param evt: resize event information
        :return: none
        """
        width = int(self.treeWidget.width() / self.treeWidget.columnCount())

        for i in range(self.treeWidget.columnCount()):
            self.treeWidget.header().resizeSection(i, width)


    def _loadTemplates(self):
        """
        Loads the templates into the start menu

        :param templates: dictionary of templates
        :return: none
        """
        for value in self.templateList.values():
            try:
                self.listWidget.addItem(QListWidgetItem(QIcon(resourcePath(value[StartMenuAttr.ICON])),
                 value[StartMenuAttr.NAME]))
            except FileNotFoundError:
                try:
                    self.listWidget.addItem(QListWidgetItem(QIcon(value[StartMenuAttr.ICON]),
                     value[StartMenuAttr.NAME]))
                except FileNotFoundError:
                    self.listWidget.addItem(QListWidgetItem(value[StartMenuAttr.NAME]))


    def _loadRecent(self) -> None:
        """
        Loads the recent projects into the start menu

        :param recent: dictionary of recent projects
        :return: none
        """

        try:
            setting = ProgSetting()
            for proj in setting.getRecentlyOpened().values():
                item = QTreeWidgetItem()
                for i in range(4):
                    item.setTextAlignment(4, Qt.AlignmentFlag.AlignCenter)

                tempProj = proj.getProperty()

                item.setText(0, tempProj["Name"])
                item.setText(1, tempProj["Author"])
                item.setText(2, tempProj["Version"])
                item.setText(3, tempProj["FN"])
                item.setText(4, tempProj["Date"])
                self.treeWidget.addTopLevelItem(item)
        except:
            pass