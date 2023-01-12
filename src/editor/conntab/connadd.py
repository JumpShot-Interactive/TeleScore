from PyQt6.QtWidgets import QTreeWidgetItem, QPushButton, QComboBox

class ConnAdd(QTreeWidgetItem):


    def __init__(self, compName, signals, compDict, tree, callback):
        super().__init__()
        self.tree = tree
        self.compName = compName
        self.signals = signals
        self.addCallBack = callback
        self.compDict = compDict

        self.sigComboBox = QComboBox()
        self.recvComboBox = QComboBox()
        self.button = QPushButton()
        
    def deleteWidget(self):
        self.tree.setItemWidget(self, 0, None)
        self.tree.setItemWidget(self, 1, None)
        self.tree.setItemWidget(self, 2, None)
        self.button.clicked.disconnect(self.buttonClicked)
        self.button.deleteLater()
        self.sigComboBox.deleteLater()
        self.recvComboBox.deleteLater()

    def _loadCombo(self):
        for i in self.signals:
            self.sigComboBox.addItem(i)

        if (len(self.signals) <= 1):
            self.sigComboBox.setDisabled(True)

        for i in self.compDict:
            recvType = self.compDict[i].getConnection().getRecvTypes()
            check = any(item in self.signals for item in recvType)
            if (i != self.compName and check):
                self.recvComboBox.addItem(i)


    def setAddCall(self, callback):
        self.addCallBack = callback


    def removedComp(self):
        self.recvComboBox.clear()
        self._loadCombo()


    def exec(self):
        self.tree.setItemWidget(self, 0, self.button)
        self.tree.setItemWidget(self, 1, self.sigComboBox)
        self.tree.setItemWidget(self, 2, self.recvComboBox)
        self.button.setText("+ ADD")
        self._loadCombo()
        self.button.clicked.connect(self.buttonClicked)


    def buttonClicked(self):
        if (len(self.recvComboBox.currentText()) > 0):
            self.addCallBack(self.recvComboBox.currentText(), self.sigComboBox.currentText())


    def removeItem(self, compName):
        self.recvComboBox.removeItem(self.recvComboBox.findText(compName))


    def addItem(self, compName):
        self.recvComboBox.addItem(compName)