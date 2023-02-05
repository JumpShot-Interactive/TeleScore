"""
Developed By: JumpShot Team
Written by: riscyseven
"""

from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

from window.editor import Editor
from window.startmenu import StartMenu
from window.settings import Settings
from window.about import About
from window.tabdialog import TabDialog
from fileio.projectfile import ProjectFile
from fileio.startfile import StartFile
from project import Project
from progsetting import ProgSetting

from gm_resources import resourcePath, GMessageBox # Importing my PyInstaller resource manager

class MainWindow(QtWidgets.QMainWindow):
    """
    This class contains the main window of the application.
    Contains the main toolbar and diverts the program to the right functionality.
    """

    def __init__(self, parent=None):
        super().__init__(parent) # Call the inherited classes __init__ method
        
        ProgSetting().loadProperties("required/data.json")
        StartFile().load()
        self.project = None
        self.tabWidget = None
        self.editor = None
        self._initUI()
        self.dialogs = []


    def _initUI(self):
        path = resourcePath("src/window/ui/mainwindow.ui") # replaced complicated path logic with resourcePath()
        uic.loadUi(path, self) # Load the .ui file
        self.setWindowTitle("TeleScore")
        self.setWindowIcon(QIcon(resourcePath("src/resources/icon.ico"))) # Using a slightly modified version of my PyInstaller Resource system. Also seen on line 18. Basically uses working directory OR temp directory for absolute paths to files.
        self.show() # Show the GUI

        # Setting up the toolbar
        self.toolBar.addWidget(QtWidgets.QPushButton(QIcon(resourcePath("src/resources/icon.ico")),
         " TeleScore v1.0.1 Beta"))
        self.toolBar.addSeparator()
        self.editModeButton = QtWidgets.QPushButton("Editor Mode")
        self.toolBar.addWidget(self.editModeButton)
        self.editModeButton.setEnabled(False)
        self.editModeButton.clicked.connect(self._editModeClicked)

        self.toolBar.addSeparator()

        self.popOutButton = QtWidgets.QPushButton("Pop Out Tab")
        self.toolBar.addWidget(self.popOutButton)
        self.popOutButton.setEnabled(False)
        self.popOutButton.clicked.connect(self._popOutClicked)

        self.actionSaveAs.triggered.connect(self._saveAsTriggered)
        self.actionOpen.triggered.connect(self._openTriggered)
        self.actionNew.triggered.connect(self._newTriggered)
        self.actionSave.triggered.connect(self._saveTriggered)
        self.actionProgSet.triggered.connect(self._settingsTriggered)
        self.actionProjSet.triggered.connect(self._projSettingsTriggered)
        self.actionAbout.triggered.connect(self._aboutTriggered)

        self.actionSave.setEnabled(False)
        self.actionSaveAs.setEnabled(False)
        self.actionProjSet.setEnabled(False)

        self.toolBar.setVisible(False)

        #self.editor = Editor()
        #self.setCentralWidget(self.editor)
        self.startMenu = StartMenu(self._newTriggered, self._openTriggered)
        self.setCentralWidget(self.startMenu)
        self._windowChanged()


    def _newTriggered(self):
        self._removeAllDialog()
        self.editor = Editor()
        self.actionSave.setEnabled(True)
        self.actionSaveAs.setEnabled(True)
        self.setCentralWidget(self.editor)

        if (self.tabWidget != None):
            self.tabWidget.deleteLater()
            self.tabWidget = None
            self.project = None
            self.toolBar.setVisible(False)
            self.editModeButton.setEnabled(False)
        self.actionProjSet.setEnabled(True)


    def _saveTriggered(self):
        if (self.editor != None):
            self.editor.saveAction()


    def _saveAsTriggered(self):
        if (self.editor != None):
            self.editor.saveAsAction()


    def _openTriggered(self, action, fileName=None):
        self._removeAllDialog()

        if (fileName == None or fileName == ""):
            self.fileName = QtWidgets.QFileDialog.getOpenFileName(self, "Open Project File", ".", "JSON File (*.json)")
        else:
            self.fileName = [fileName, "JSON File (*.json)"]

        self.actionSave.setEnabled(False)
        self.actionSaveAs.setEnabled(False)
        self.actionProjSet.setEnabled(False)

        if (self.fileName[0] != "" and self.fileName[1] == "JSON File (*.json)"):
            self.editor = None
            try:
                self.tabWidget = QtWidgets.QTabWidget()
                self.tabWidget.setMovable(True)
                self.project = Project()
                self.project.setFileName(self.fileName[0])
                ProjectFile(self.project).load()
                self.project.setFileName(self.fileName[0])

                for tabName, tab in self.project.getAllLO().items():
                    if (tab.getProperty()["Pop Out On Start"]):
                        self._createNewDialog(tab)
                    else:
                        self.tabWidget.addTab(tab, tabName)

                self.setCentralWidget(self.tabWidget)
                self.toolBar.setVisible(True)
                self.editModeButton.setEnabled(True)
                self._enablePopOutButton()

                self.project.setDate()
                ProgSetting().addRecentlyOpened(self.project)

            except Exception as ex:
                GMessageBox("Project File Load Error",
                 f"This file may be corrupted or not a valid project file.\nPlease try again.\n{ex}",
                  "Info", self).exec()

                self.toolBar.setVisible(False)
                try:
                    self.setCentralWidget(self.startMenu)
                except RuntimeError:
                    self.startMenu = StartMenu(self._newTriggered, self._openTriggered)
                    self.setCentralWidget(self.startMenu)


    def _settingsTriggered(self):
        settings = Settings(ProgSetting().getProperties(), self)
        if  (settings.exec() == settings.DialogCode.Accepted):
            self._windowChanged()
            ProgSetting().saveProperties("required/data.json")


    def _projSettingsTriggered(self):
        settings = Settings(self.editor.getProject().getProperty(), self)
        if (settings.exec() == settings.DialogCode.Accepted):
            self.editor.getProject().saveProperties()


    def _aboutTriggered(self):
        About(self).exec()


    def _enablePopOutButton(self):
        if (self.tabWidget.count() > 0):
            self.popOutButton.setEnabled(True)
        else:
            self.popOutButton.setEnabled(False)


    def _editModeClicked(self):
        self._removeAllDialog()
        self.editor = Editor(self.project)
        self.tabWidget.deleteLater()
        self.tabWidget = None
        self.project = None
        self.toolBar.setVisible(False)
        self.editModeButton.setEnabled(False)
        self.actionSave.setEnabled(True)
        self.actionSaveAs.setEnabled(True)
        self.actionProjSet.setEnabled(True)
        self.setCentralWidget(self.editor)

    
    def _createNewDialog(self, tab):
        dialog = TabDialog(tab, self._popOutTabClosed, self)
        dialog.setWindowTitle(tab.objectName())
        dialog.show()
        self.dialogs.append(dialog)


    def _removeAllDialog(self):
        for dialog in self.dialogs:
            dialog.deleteLater()
        self.dialogs = []

    
    def _popOutClicked(self):
        tab = self.tabWidget.currentWidget()

        tab.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self._createNewDialog(tab)
        tab.setVisible(True)

        if (self.tabWidget.count() == 0):
            self.popOutButton.setEnabled(False)


    def _popOutTabClosed(self, tab):
        self.tabWidget.addTab(tab.getTab(), tab.getTab().objectName())
        self._enablePopOutButton()
        self.dialogs.remove(tab)


    def closeEvent(self, evt) -> None:
        StartFile().save()
        if (self.editor != None):
            if (self.editor.closingDialog()):
                evt.accept()
            else:
                evt.ignore()


    def _windowChanged(self):
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, ProgSetting().getProperties()["Always On Top"])
        self.show()