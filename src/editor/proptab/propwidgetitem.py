"""
Developed By: JumpShot Team
Written by: riscyseven
"""

from PyQt6.QtWidgets import QWidget, QTreeWidgetItem, QColorDialog
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt

from editor.proptab.propwidgetfactory import PropWidgetFactory

class PropWidgetItem(QTreeWidgetItem):
    """
    Each component listed in the component list is made from 
    this class object. This widget item will standardize attributes
    such as the fonts, icon image size, etc.
    """

    def __init__(self, parent, prop, callBack, treeWidget=None):
        """
        Consturctor for a component list item

        :param icon: Icon for the component
        :param parent: Header/category of the item
        :param treeWidget: Main component list widget
        :param text: Description of the component

        :return: none
        """
        super().__init__(parent) # This sets this component to be the subcomponent of the header
        self.setText(0, prop.getName())
        self.setTextAlignment(0, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        self.setFont(0, QFont("Segoe UI", 11))
        self.editWidget = PropWidgetFactory.createProp(prop.getType(), prop.getValue(), prop.getOption(), self)
        self.editWidget.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
        if (treeWidget != None):
            self._treeWidget = treeWidget
        else:
            self._treeWidget = parent
        self.callBack = callBack
        self._prop = prop


    def deleteWidget(self):
        self.editWidget.deleteLater()
        self.editWidget = None


    def getWidget(self) -> QWidget:
        return self.editWidget


    def _spinBoxChanged(self, value: int):
        self.callBack(self._prop, value)


    def _lineEditChanged(self, value: str):
        self.callBack(self._prop, value)


    def _fontEditChanged(self, font: QFont):
        self.callBack(self._prop, font.family())


    def _checkBoxChanged(self, checked: int):
        self.callBack(self._prop, checked)

    
    def _fileSctClicked(self, fileName):
        self.callBack(self._prop, fileName)


    def _hotKeyFinished(self, hotKey):
        self.callBack(self._prop, hotKey)


    def _createColorDialog(self):
        color = QColorDialog(QColor(self._prop.getValue()), self._treeWidget)
        if (color.exec() == QColorDialog.DialogCode.Accepted):
            self.callBack(self._prop, color.currentColor().name())
            self.editWidget.setStyleSheet(f"background-color:{color.currentColor().name()}")
        color.deleteLater()

    
    def _comboBoxChanged(self, index: int):
        self.callBack(self._prop, index)