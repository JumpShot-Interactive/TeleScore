"""
Developed By: JumpShot Team
Written by: riscyseven
"""

from PyQt6.QtWidgets import QMainWindow, QFrame, QFileDialog, QPushButton, QMessageBox
from PyQt6 import uic, QtGui
from PyQt6.QtCore import QPoint, pyqtSlot, Qt
from gm_resources import resourcePath, GMessageBox

from abstract.abstractcomp import AbstractComp
from editor.complisttab import CompListTab
from editor.propertytab import PropertyTab
from editor.conntab.connman import ConnMan
from editor.savedialog import SaveDialog
from editor.activetab import ActiveTab

from abstract.layoutcomp import LayoutComp
from editor.command.insertcmd import InsertCmd
from editor.command.inserttlocmd import InsertLOCmd
from editor.command.deletelocmd import DeleteLOCmd
from project import Project
from fileio.projectfile import ProjectFile
from attr import CompType
from window.tabdialog import TabDialog
from progsetting import ProgSetting


class Editor(QMainWindow):
    def __init__(self, project: Project=None, parent=None):
        super().__init__(parent) # Call the inherited classes __init__ method
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
        self.cmdStack = QtGui.QUndoStack(self) # Command stack used for undo/redo
        self.currComp = None
        self.currLO = None

        self._initUI(project)


    def _loadProject(self, project: Project):
        """
        Loads a project into the editor.

        :param project: The project to load.
        :return: none
        """
        self.project = project

        for tab in self.project.getAllLO().values():
            self.tabWidget.addTab(tab, tab.objectName())
            tab.getLayout().setRemoveCallBack(self._remCallBack)
            tab.getLayout().setDropCallBack(self._dropSlot)
            for comp in tab.getLayout().getLOComp():
                if comp.getType() == CompType.CONTROL:
                    comp.setEditorMode(True)
                comp.compClicked.connect(self._compClicked)
            tab.LOClicked.connect(self._compClicked)


    def _initUI(self, project) -> None:
        """
        Initializes the editor UI.

        :param: none
        :return: none
        """
        uic.loadUi(resourcePath("src/window/ui/editor.ui"), self) # Load the .ui file

        if project is None:
            self.project = Project()
            tab = InsertLOCmd(self.project, self.tabWidget, self._remCallBack, self._dropSlot)
            self.cmdStack.push(tab)
            tab.getLayout().LOClicked.connect(self._compClicked)
        else:
            self._loadProject(project)

        self.project.addLORenameCallBack(self._renameCallBack)
            
        self.project.setEditMode(True)
        self.project.setInEditor(True)

        self.comp = CompListTab(self)
        self.compDock.setWidget(self.comp)

        self.prop = PropertyTab(self)
        self.propDock.setWidget(self.prop)

        self.conn = ConnMan(self.project, self)
        self.connDock.setWidget(self.conn)

        self.acti = ActiveTab(self.project, self)
        self.actiDock.setWidget(self.acti)
        self._compClicked(self.tabWidget.widget(0))

        # Setting up the toolbar

        # This is a bit redundant. If there is a simpler way of doing this, please change it.
        self.toolBar.addWidget(QPushButton(QtGui.QIcon(resourcePath("src/resources/icon.ico")),
         " TeleScore v1.0.1 Beta"))
        self.toolBar.addSeparator()
        self.addTabPushButton = QPushButton("Add Tab")
        self.toolBar.addWidget(self.addTabPushButton)
        self.addTabPushButton.clicked.connect(self._addTab)
        self.tabWidget.tabBarClicked.connect(self._tabClicked)
        self.removeTabPushButton = QPushButton("Remove Tab")
        self.toolBar.addWidget(self.removeTabPushButton)
        self.removeTabPushButton.clicked.connect(self._removeTab)
        self.removeTabPushButton.setEnabled(False)

        self.toolBar.addSeparator()
        self.toolBar.addSeparator()
        self.editModePushButton = QPushButton("Edit Mode")
        self.editModePushButton.setEnabled(False)
        self.toolBar.addWidget(self.editModePushButton)
        self.editModePushButton.clicked.connect(self._editMode)
        self.viewModePushButton = QPushButton("View Mode")
        self.toolBar.addWidget(self.viewModePushButton)
        self.viewModePushButton.clicked.connect(self._viewMode)

        self.toolBar.addSeparator()
        self.toolBar.addSeparator()

        self.popOutTabPushButton = QPushButton("Pop Out Tab")
        self.toolBar.addWidget(self.popOutTabPushButton)
        self.popOutTabPushButton.clicked.connect(self._popOutTab)

        self._refreshTabButton()


    def getProject(self) -> Project:
        """
        Returns the project.

        :param: none
        :return: The project.
        """
        return self.project


    @pyqtSlot(bool)
    def _viewMode(self, clicked):
        """
        Switches the editor to view mode.

        :param clicked: Whether the button was clicked.
        :return: none
        """
        self.project.setEditMode(False)
        self.editModePushButton.setEnabled(True)
        self.viewModePushButton.setEnabled(False)
        self.clearCurrComp()


    @pyqtSlot(bool)
    def _editMode(self, clicked):
        """
        Switches the editor to edit mode.

        :param clicked: Whether the button was clicked.
        :return: none
        """
        self.project.setEditMode(True)
        self.editModePushButton.setEnabled(False)
        self.viewModePushButton.setEnabled(True)


    @pyqtSlot(int)
    def _tabClicked(self, index):
        self._compClicked(self.tabWidget.widget(index))


    @pyqtSlot(bool)
    def _addTab(self, clicked):
        cmd = InsertLOCmd(self.project, self.tabWidget, self._remCallBack, self._dropSlot)
        self.cmdStack.push(cmd)
        
        self._refreshTabButton()

        cmd.getLayout().LOClicked.connect(self._compClicked)


    @pyqtSlot(bool)
    def _removeTab(self, clicked):
        msg = GMessageBox("Are you sure?", "Are you sure you want to remove this tab?", "AskYesNo", self)
        if (msg.exec() == QMessageBox.StandardButton.Yes):
            self.clearCurrComp()
            self.clearActiveTab()
            cmd = DeleteLOCmd(self.project, self.tabWidget.currentIndex(), self.tabWidget)
            self.cmdStack.push(cmd)

            self._refreshTabButton()


    def _renameCallBack(self, fromName, toName):
        for i in range(self.tabWidget.count()):
            if (self.tabWidget.tabText(i) == fromName):
                self.tabWidget.setTabText(i, toName)


    def _popOutTab(self, clicked):
        tab = self.tabWidget.currentWidget()
        self.clearCurrComp()

        dialog = TabDialog(tab, self._popOutTabClosed, self)
        dialog.setWindowTitle(tab.objectName())
        dialog.show()

        tab.setVisible(True)
        self._refreshTabButton()


    def _popOutTabClosed(self, tab):
        self.clearCurrComp()
        self.tabWidget.addTab(tab.getTab(), tab.getTab().objectName())
        self._refreshTabButton()


    def _refreshTabButton(self):
        if (self.tabWidget.count() > 1):
            self.removeTabPushButton.setEnabled(True)
        else:
            self.removeTabPushButton.setEnabled(False)
    
        if (self.tabWidget.count() > 0):
            self.popOutTabPushButton.setEnabled(True)
        else:
            self.popOutTabPushButton.setEnabled(False)


    @pyqtSlot(object)
    def _compClicked(self, comp: AbstractComp) -> None:
        """
        If any of the component is clicked, this
        slot gets called. This should process the property
        tab initiation. Get the property of the component
        and pass it onto the property tab.

        :param comp: Component that has been clicked
        :return: none
        """
        if (self.currComp != comp):
            self.clearCurrComp()
            self.prop.propChanged.connect(comp.propChanged)
            self.prop.loadPropertyFromComp(comp)
            comp.attrChanged.connect(self.prop.externalChange)

            if (comp.getType() != CompType.LAYOUT):
                comp.setFrameShape(QFrame.Shape.Box)
                comp.setLineWidth(3)
            else:
                self.clearActiveTab()
                self.currLO = comp
                self.acti.initTable(comp)
                comp.getLayout().actiUpdate.connect(self.acti.update)

            if (isinstance(comp, LayoutComp)):
                self.conn.setComp(comp)

        self.currComp = comp


    def clearCurrComp(self):
        if (self.currComp != None):
            self.prop.clearTree()
            self.conn.clearTable()
            self.prop.propChanged.disconnect(self.currComp.propChanged)
            self.currComp.attrChanged.disconnect(self.prop.externalChange)
            self.currComp.setFrameShape(QFrame.Shape.NoFrame)
            self.currComp = None


    def clearActiveTab(self):
        if (self.currLO != None):
            self.acti.clearTable()
            self.currLO.getLayout().actiUpdate.disconnect(self.acti.update)
            self.currLO = None


    def _dropSlot(self, evt: QtGui.QDropEvent, layout):
        """
        When component is dropped from the components list, 
        this is called and adds the right component to the layout

        :param evt: event information
        :return: none
        """
        # I could put this inside the layout but more unnecessary code for layout
        type = evt.mimeData().data("application/x-comp").data().decode()
        point = QPoint(int(evt.position().x()), int(evt.position().y()))
        insert = InsertCmd(self.project, layout, type, point)
        self.cmdStack.push(insert)

        insert.getComp().compClicked.connect(self._compClicked)


    def _remCallBack(self, component: AbstractComp):
        if (self.currComp == component):
            self.clearCurrComp()
        component.compClicked.disconnect(self._compClicked)


    def saveAction(self):
        if (self.project.getFileName() != ""):
            ProjectFile(self.project).save()
            self.project.setDate()
            ProgSetting().addRecentlyOpened(self.project)
        else:
            self.saveAsAction()


    def saveAsAction(self):
        file = QFileDialog.getSaveFileName(self, "Save Layout File As", ".", "JSON File (*.json)")

        if (file[0] != '' and file[1] != ''):
            self.project.setFileName(file[0])
            ProjectFile(self.project).save()
            self.project.setDate()
            ProgSetting().addRecentlyOpened(self.project)


    # Override
    def keyPressEvent(self, evt: QtGui.QKeyEvent) -> None:
        '''if (evt.modifiers() & Qt.KeyboardModifier.ControlModifier):
            match evt.key():
                case Qt.Key.Key_Z:
                    self.cmdStack.undo()'''
        if (evt.modifiers() & Qt.KeyboardModifier.ControlModifier):
            match evt.key():
                case Qt.Key.Key_S:
                    self.saveAction()

        evt.accept()


    def closingDialog(self) -> bool:
        dialog = SaveDialog(self)
        if (dialog.exec() == dialog.DialogCode.Accepted):
            self.saveAction()
        elif (dialog.getCode() == dialog.CANCEL):
            return False

        return True
