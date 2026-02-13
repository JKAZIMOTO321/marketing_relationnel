from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
from gui.ui_achatWindow import Ui_Form
from services.achats_services import AchatsServices
from .utilitaires import (ajusterColonnesDansTables, 
                          chargerClientsDansComboBox,
                          afficher_alerte,
                          afficher_information)
class AchatsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.tableaux = [self.ui.tableWidget]
        self.achatsS = AchatsServices()
        ajusterColonnesDansTables(listTables=self.tableaux)
        self.chargerCB()
        self.chargerDonneesDansTable()
        self.ui.btnEnreigistrer.clicked.connect(self.enregistrerAchat)

    def chargerCB(self):
        chargerClientsDansComboBox(self.ui.comboBox_NomClient)

    def enregistrerAchat(self):
        try:
            idClient = int(self.ui.comboBox_NomClient.currentData())
            montant = float(self.ui.doubleSpinBoxMontant.value())
            self.achatsS.enregistrerAchat(idClient=idClient, Montant=montant)
            afficher_information(message="Succès !")
            self.chargerDonneesDansTable()
        except Exception as e:
            afficher_alerte(message=f"Erreur : {e}")

    def chargerDonneesDansTable(self):
        table = self.ui.tableWidget
        donnees = self.achatsS.db.get_achats_ClientName()
        table.setRowCount(len(donnees))
        
        for row, achat in enumerate(donnees):
            #colone 0 ID
            table.setItem(row,0,self._create_item(achat.get("ClientID", "")))
            table.setItem(row,1,self._create_item(achat.get("ClientName", "")))
            table.setItem(row,2,self._create_item(achat.get("Montant", "")))
            
            date_valeur = achat.get("DateAchat", "")
            if date_valeur:
                date_valeur = date_valeur.strftime("%d/%m/%Y %H:%M")
            table.setItem(row,3,self._create_item(date_valeur))
            

    def _create_item(self, value):
        item = QTableWidgetItem(str(value))
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
        return item




    
