"""
Developed By: JumpShot Team
Written by: riscyseven
"""

from PyQt6.QtWidgets import QTreeWidgetItem, QPushButton, QLineEdit

class ConnRem(QTreeWidgetItem):
    def __init__(self, compName, signal, tree, callback):
        super().__init__()
        self.tree = tree
        self.remCallBack = callback

        self.button = QPushButton()
        self.sigLineEdit = QLineEdit(signal)
        self.sigLineEdit.setEnabled(False)
        self.recvLineEdit = QLineEdit(compName)
        self.recvLineEdit.setEnabled(False)

    def deleteWidget(self):
        self.tree.setItemWidget(self, 0, None)
        self.tree.setItemWidget(self, 1, None)
        self.tree.setItemWidget(self, 2, None)
        self.button.clicked.disconnect(self.buttonClicked)
        self.button.deleteLater()
        self.sigLineEdit.deleteLater()
        self.recvLineEdit.deleteLater()
        

    def exec(self):
        self.tree.setItemWidget(self, 0, self.button)
        self.tree.setItemWidget(self, 1, self.sigLineEdit)
        self.tree.setItemWidget(self, 2, self.recvLineEdit)
        self.button.setText("- REMOVE")

        self.button.clicked.connect(self.buttonClicked)


    def buttonClicked(self):
        self.remCallBack(self.recvLineEdit.text(), self.sigLineEdit.text(), self)
