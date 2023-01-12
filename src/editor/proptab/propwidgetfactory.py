
from editor.proptab.fileseldialog import FileSelWidget
from editor.conntab.hotkeyman import HotkeyMan
from editor.proptab.proplineedit import PropLineEdit
from attr import PropWidgetType

from PyQt6.QtWidgets import QWidget, QSpinBox, QFontComboBox, QCheckBox, QPushButton, QComboBox
from PyQt6.QtGui import QFont

class PropWidgetFactory:
    
    """ Factory class for creating property widgets. """

    @classmethod
    def createProp(self, text, value, option, slot) -> QWidget:
        wid = None
        match text:
            case PropWidgetType.TEXTEDIT:
                wid = self._createTextEdit(value, slot._lineEditChanged)
            case PropWidgetType.NUMEDIT:
                wid = self._createNumEdit(value, slot._spinBoxChanged)
            case PropWidgetType.FONTEDIT:
                wid = self._createFontEdit(value, slot._fontEditChanged)
            case PropWidgetType.CHECKBOX:
                wid = self._createCheckBox(value, slot._checkBoxChanged)
            case PropWidgetType.FLSAVE | PropWidgetType.FLOPEN:
                wid = self._createFileSct(text, value, slot._fileSctClicked)
            case PropWidgetType.HOTEDIT:
                wid = self._createHotKeyMan(value, slot._hotKeyFinished)
            case PropWidgetType.COLORPICK:
                wid = self._createColorEdit(value, slot._createColorDialog)
            case PropWidgetType.COMBOBOX:
                wid = self._createComboBox(option, value, slot._comboBoxChanged)
            case PropWidgetType.DRSAVE:
                wid = self._createFileSct(text, value, slot._fileSctClicked)
        return wid


    @classmethod
    def _createTextEdit(self, value, slot):
        """
        Creates a new QLineEdit widget to insert
        to the treeview

        :param: none (might change in the future for some attribute changes)
        :return: none
        """
        lineEdit = PropLineEdit(value, slot)
        return lineEdit


    @classmethod
    def _createFontEdit(self, value, slot):
        """
        Creates a new QPushButton widget to insert
        to the treeview, this pushbutton will open a font dialog

        :param: none (might change in the future for some attribute changes)
        :return: none
        """
        edit = QFontComboBox()
        edit.setCurrentFont(QFont(value))
        edit.currentFontChanged.connect(slot)
        return edit


    @classmethod
    def _createNumEdit(self, value, slot) -> QSpinBox:
        """
        Creates a new QSpinbox widget to insert
        to the treeview. Restricted to only numbers

        :param: none (might change in the future for some attribute changes)
        :return: none
        """
        spinBox = QSpinBox()
        spinBox.setMinimum(0)
        spinBox.setMaximum(9999999)
        spinBox.setValue(value)
            
        spinBox.valueChanged.connect(slot)
        return spinBox


    @classmethod
    def _createCheckBox(self, value, slot) -> QCheckBox:
        wid = QCheckBox()
        wid.setChecked(value)
        wid.stateChanged.connect(slot)
        return wid


    @classmethod
    def _createFileSct(self, mode, value, slot) -> QPushButton:
        wid = FileSelWidget(mode, slot, value)
        self.fileName = value
        return wid


    @classmethod
    def _createHotKeyMan(self, value, slot):
        wid = HotkeyMan(value, slot)
        return wid


    @classmethod
    def _createColorEdit(self, value, slot):
        wid = QPushButton("Pick Color")
        wid.setStyleSheet(f"background-color:{value}")
        self.color = value # Maybe refractor this in the future
        wid.clicked.connect(slot)
        return wid


    @classmethod
    def _createComboBox(self, option, value, slot):
        wid = QComboBox()
        wid.addItems(option)
        wid.setCurrentIndex(value)
        wid.currentIndexChanged.connect(slot)
        return wid