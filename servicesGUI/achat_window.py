from PyQt5.QtWidgets import QWidget
from gui.ui_achatWindow import Ui_Form
from utilitaires import ajusterColonnesDansTables
class AchatsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.tableaux = [self.ui.tableWidget]
        ajusterColonnesDansTables(listTables=self.tableaux)
