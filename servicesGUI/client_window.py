from PyQt5.QtWidgets import QWidget
from gui.ui_clientWindow import Ui_Form

class ClientPage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)