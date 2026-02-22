from PyQt5.QtWidgets import QWidget
from gui.ui_commissionWindow import Ui_Form
from utilitaires import ajusterColonnesDansTables
class CommissionPage(QWidget):
    def __init__(self, idClient=None):
        super().__init__()
        self.ui = Ui_Form()
        self.idClient = idClient
        self.ui.setupUi(self)
        tables = [self.ui.tableFilleulDirect, self.ui.tableFilleulIndirect]
        ajusterColonnesDansTables(tables)

    