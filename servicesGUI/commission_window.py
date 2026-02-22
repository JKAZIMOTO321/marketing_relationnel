from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from gui.ui_commissionWindow import Ui_Form
from services.commissions_service import CommissionService
from .utilitaires import ajusterColonnesDansTables

class CommissionPage(QWidget):
    def __init__(self, idClient=None):
        super().__init__()
        self.ui = Ui_Form()
        self.idClient = idClient
        self.service = CommissionService()
        self.ui.setupUi(self)
        tables = [self.ui.tableFilleulDirect, self.ui.tableFilleulIndirect]
        ajusterColonnesDansTables(tables)
        if  self.idClient:
            self.charger_commissions()

    def charger_commissions(self):
        directs, indirects = self.service.get_commissions_details(self.idClient)

        self.ui.lblNomsClient.setText(self.service.get_nomClient(idClient=self.idClient))

        self.remplir_table(self.ui.tableFilleulDirect, directs)
        self.remplir_table(self.ui.tableFilleulIndirect, indirects)

        total_direct = sum(c[2] for c in directs)
        total_indirect = sum(c[2] for c in indirects)
        total_general = total_direct + total_indirect

        self.ui.lineEdit_Tot_Comm_direct.setText(str(total_direct))
        self.ui.lineEdit_Tot_Comm_indirect.setText(str(total_indirect))
        self.ui.lblTotCommissions.setText(str(total_general))


    def remplir_table(self, table, data):
        table.setRowCount(len(data))

        for row, (client_id, total_achat, commission) in enumerate(data):
            table.setItem(row, 0, QTableWidgetItem(str(client_id)))
            table.setItem(row, 1, QTableWidgetItem(str(total_achat)))
            table.setItem(row, 2, QTableWidgetItem(str(commission)))