from sys import exception
from PyQt5.QtWidgets import QWidget
from gui.ui_relationWindow import Ui_Form
from services.relations_services import RelationService
from .utilitaires import (ajusterColonnesDansTables,
                          _create_item, chargerClientsDansComboBox, afficher_alerte,
                          afficher_information)

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
        self.ui.btnAjouter.clicked.connect(self.ajouterRelation)
        self.ui.btnActualiser.clicked.connect(self.chargerDonneesDansTable)

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

    def ajouterRelation(self):
        parrain = self.ui.comboBox_AddParrain.currentData()
        filleul = self.ui.comboBox_AddFilleul.currentData()
        #Empecher l'insertion de la relation si elle creerait un cycle
        if self.relService.relationCreeraitCycle(parrainID=parrain, filleulID=filleul):
            afficher_alerte("Erreur : Cette relation Creerait un cycle dans le reseau")
            return
        try:
            self.relService.db.add_relation(parrainID=parrain, filleulID=filleul)
            afficher_information("Ajout de la relation effectué avec succès")
        except Exception as e:
            afficher_alerte(f"Erreur :{e}")
        self.chargerDonneesDansTable()
    


        



