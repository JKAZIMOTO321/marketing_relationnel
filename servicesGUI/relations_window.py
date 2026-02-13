from sys import exception
from PyQt5.QtWidgets import QWidget
from gui.ui_relationWindow import Ui_Form
from services.relations_services import RelationService
from .utilitaires import (ajusterColonnesDansTables,
                          _create_item, chargerClientsDansComboBox)

class RelationsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.relService = RelationService()
        self.tableaux = [self.ui.tableWidget]
        ajusterColonnesDansTables(self.tableaux)
        self.chargerDonneesDansTable()
        self.chargerCBParrain()
        self.chargerCBFilleul()
        self.ui.comboBox_AddParrain.currentTextChanged.connect(self.chargerCBFilleul)

    def chargerDonneesDansTable(self):
        table = self.ui.tableWidget
        donnees = self.relService.get_data_tableau()
        table.setRowCount(len(donnees))

        for row, relation in enumerate(donnees):
            table.setItem(row, 0, _create_item(relation.get("parrainID","")))
            table.setItem(row, 1, _create_item(relation.get("NomParrain","")))
            table.setItem(row, 2, _create_item(relation.get("filleulID","")))
            table.setItem(row, 3, _create_item(relation.get("NomFilleul","")))
            date = relation.get("Date", "")
            if date:
                date = date.strftime("%d/%m/%Y %H:%M")
            table.setItem(row,4,_create_item(date))
    
    def chargerCBParrain(self):
        chargerClientsDansComboBox(ComboBox=self.ui.comboBox_AddParrain)
    
    def chargerCBFilleul(self):
        idParrain = self.ui.comboBox_AddParrain.currentData()
        self.ui.comboBox_AddFilleul.clear()
        chargerClientsDansComboBox(ComboBox=self.ui.comboBox_AddFilleul,
                                   exceptOne=True, 
                                   idToExcept=idParrain)



