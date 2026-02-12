from PyQt5.QtWidgets import QWidget
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
        self.ui.btnEnreigistrer.clicked.connect(self.enregistrerAchat)

    def chargerCB(self):
        chargerClientsDansComboBox(self.ui.comboBox_NomClient)

    def enregistrerAchat(self):
        try:
            idClient = int(self.ui.comboBox_NomClient.currentData())
            montant = float(self.ui.doubleSpinBoxMontant.value())
            self.achatsS.enregistrerAchat(idClient=idClient, Montant=montant)
            afficher_information(message="Succès !")
        except Exception as e:
            afficher_alerte(message=f"Erreur : {e}")

    def chargerDonneesDansTable(self):
        table = self.ui.tableWidget



    
