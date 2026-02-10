from PyQt5.QtWidgets import QWidget
from gui.ui_commissionWindow import Ui_Form

class CommissionPage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)