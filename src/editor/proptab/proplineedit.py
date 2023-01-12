from PyQt6.QtWidgets import QPushButton, QLineEdit, QWidget, QHBoxLayout

class PropLineEdit(QWidget):
    def __init__(self, text, callback, parent=None):
        super().__init__(parent)
        self._callback = callback
        self._text = text
        self._initUI()


    def _initUI(self):
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(2)
        self._lineEdit = QLineEdit(self._text)
        self._button = QPushButton("Done")
        self._layout.addWidget(self._lineEdit)
        self._layout.addWidget(self._button)
        self._button.clicked.connect(self._buttonClicked)
        self._lineEdit.returnPressed.connect(self._buttonClicked)


    def _buttonClicked(self):
        self._callback(self._lineEdit.text())


    def propertyMode(self):
        self._lineEdit.textEdited.connect(self._callback)
        self._button.setVisible(False)