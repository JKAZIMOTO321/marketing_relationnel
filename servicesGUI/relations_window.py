from sys import exception
from PyQt5.QtWidgets import QWidget
from gui.ui_relationWindow import Ui_Form

class RelationsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)