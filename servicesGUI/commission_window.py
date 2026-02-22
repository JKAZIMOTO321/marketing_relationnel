from PyQt5.QtWidgets import QWidget, QTableWidgetItem
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

    def remplir_table(self, table, data):
        table.setRowCount(len(data))

        for row, (client_id, total_achat, commission) in enumerate(data):
            table.setItem(row, 0, QTableWidgetItem(str(client_id)))
            table.setItem(row, 1, QTableWidgetItem(str(total_achat)))
            table.setItem(row, 2, QTableWidgetItem(str(commission)))