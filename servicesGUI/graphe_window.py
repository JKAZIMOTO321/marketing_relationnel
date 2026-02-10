from PyQt5.QtWidgets import QWidget
from gui.ui_grapheWindow import Ui_Form

class GraphePage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)