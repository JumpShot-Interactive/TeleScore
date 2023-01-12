"""
Developed By: JumpShot Team
Written by: riscyseven
"""

from PyQt6.QtWidgets import QWidget
from PyQt6 import uic

from editor.conntab.connadd import ConnAdd
from editor.conntab.connrem import ConnRem
from gm_resources import resourcePath

class ConnMan(QWidget):
    def __init__(self, project, parent=None):
        super().__init__(parent)
        path = resourcePath("src/editor/conntab/connman.ui")
        uic.loadUi(path, self) # Load the .ui file
        
        self._project = project

    def setComp(self, comp):
        self.clearTable()
        self._compName = comp.objectName()
        self._connection = comp.getConnection()
        self.initTable()


    def initTable(self):
        expanded = self._connection.getData()
        self.A2B = expanded[0]
        self.B2A = expanded[1]

        self.addItem = ConnAdd(self._compName, self._connection.getSignalTypes(), 
            self._project.getAllComp(), self.treeWidget, self._addA2BCallBack)
        self.treeWidget.addTopLevelItem(self.addItem)
        self.addItem.exec()

        for type in self.A2B:
            for comp in self.A2B[type]:
                self._addA2BCallBack(comp.objectName(), type, True)
 
        for tuple in self.B2A:
            self._addB2ACallBack(tuple[0].objectName(), tuple[1], True)


    def clearTable(self):
        while self.treeWidget.topLevelItemCount() > 0:
            item = self.treeWidget.takeTopLevelItem(0)
            item.deleteWidget()
            del item
        
        while self.treeWidget_2.topLevelItemCount() > 0:
            item = self.treeWidget_2.takeTopLevelItem(0)
            item.deleteWidget()
            del item


    def _addA2BCallBack(self, recvCompName: str, signal: str, init=False):
        comp = self._project.getComp(recvCompName)
        if (comp not in self.A2B[signal] or init): # Check to make sure we are not duplicating, assuming signal exists for the connected comp
            connInst = ConnRem(recvCompName, signal, self.treeWidget, self._remA2BCallBack)
            self.treeWidget.addTopLevelItem(connInst)
            connInst.exec()
            if (init == False):
                self.A2B[signal].append(comp)
            self.addItem.removeItem(recvCompName)
            self._connection.dataChanged()


    def _addB2ACallBack(self, sigCompName: str, signal: str, init=False):
        connInst = ConnRem(sigCompName, signal, self.treeWidget_2, self._remB2ACallBack)
        self.treeWidget_2.addTopLevelItem(connInst)
        connInst.exec()
        self._connection.dataChanged()


    def _remA2BCallBack(self, recvCompName: str, signal: str, inst: ConnRem):
        comp = self._project.getComp(recvCompName)
        self.A2B[signal].remove(comp)
        self.treeWidget.takeTopLevelItem(self.treeWidget.indexOfTopLevelItem(inst))
        self.addItem.addItem(recvCompName)
        self._connection.dataChanged()


    def _remB2ACallBack(self, sigCompName: str, signal: str, inst: ConnRem):
        comp = self._project.getComp(sigCompName)
        self.treeWidget_2.takeTopLevelItem(self.treeWidget_2.indexOfTopLevelItem(inst))
        self.B2A.remove((comp, signal))
        self._connection.dataChanged()

            




    
