from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QMessageBox, QTableWidgetItem
from gui.ui_clientWindow import Ui_Form
from services.client_services import ClientsService
from .utilitaires import (demanderConfirmation, afficher_alerte, 
                          afficher_information, nettoyerLineEdit, 
                          ajusterColonnesDansTables)

class ClientPage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        ajusterColonnesDansTables([self.ui.tableWidget])
        self.clientService = ClientsService()
        self.colonnesTables =[
            ("ClientID", "ID"),
            ("ClientName", "Nom complet"),
            ("Email", "Email"),
            ("Phone", "Téléphone"),
            ("DateInscription", "Date inscription"),
            ("Statut", "Statut"),
        ]
        self.chargerDonneesDansTable()
        self.chargerParrainsComboBox(self.ui.comboBox_AddParrain)
        self.elementsAdd = [self.ui.lineEdit_AddNom, self.ui.lineEdit_AddEmail, self.ui.lineEdit_AddTel]
        self.elementsMod = [
            self.ui.lineEdit_ModifNom,
            self.ui.lineEdit_ModEmail,
            self.ui.lineEdit_ModTel
        ]
        self.ui.btn_Ajouter.clicked.connect(self.ajouterClient)
        self.ui.tableWidget.itemSelectionChanged.connect(self.remplirChampsModifierSelection)
        # self.ui.btn_Actualiser.clicked.connect(self.remplirChampsModifierSelection)


    def ajouterClient(self):
        donnees ={
            "nom" : self.ui.lineEdit_AddNom.text().strip(),
            "email" : self.ui.lineEdit_AddEmail.text().strip(),
            "phoneNumber" : self.ui.lineEdit_AddTel.text().strip()
        }
        parrain = self.ui.comboBox_AddParrain.currentData()
        for element, valeur in donnees.items():
            if valeur=="":
                afficher_alerte(f"Veuillez d'abord remplir le champ {element}")
                return
        # demande de confirmation
        confirmation = demanderConfirmation(
            fenetre=self,
            messageDemande="Voulez-vous enregistrer ces données ?"
        )
        if confirmation:
            ajout = self.clientService.ajouterClient(
                Nom=donnees["nom"],
                Email=donnees["email"],
                Phone=donnees["phoneNumber"],
                Parrain=parrain
            )
            if ajout:
                afficher_information(message="Ajout du client effectué avec succès")
            if not ajout:
                afficher_alerte(message="Echec de l'enregistrement")
            nettoyerLineEdit(self.elementsAdd)

    def chargerParrainsComboBox(self, ComboBox):
        ComboBox.clear()
        ComboBox.addItem("Aucun Parrain", None)
        #depuis la BDD
        clients = self.clientService.recupererNomId()
        for client in clients:
            client_id = client["ClientID"]
            clientNom = client["ClientName"]
            ComboBox.addItem(
                clientNom,
                client_id
            )

    def chargerDonneesDansTable(self):
        table = self.ui.tableWidget
        clients = self.clientService.data.get_clients()
        table.setRowCount(len(clients))
        table.setColumnCount(len(self.colonnesTables))
        table.setHorizontalHeaderLabels([label for _, label in self.colonnesTables])

        for row, client in enumerate(clients):
            for col, (key, _) in enumerate(self.colonnesTables):
                value = client.get(key, "")

                # Format date
                if key == "DateInscription" and value:
                    value = value.strftime("%d/%m/%Y %H:%M")

                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)  # lecture seule

                table.setItem(row, col, item)

    def remplirChampsModifierSelection(self):
        # 1. Obtenir l'indice de la ligne sélectionnée
        ligne = self.ui.tableWidget.currentRow()
        if ligne<0 :
            afficher_alerte(message="Aucun element selectionnee")
            return

        # 2. Extraire les données des colonnes (0, 1, 2, etc.)
        # .text() permet de récupérer la chaîne de caractères
        id = self.ui.tableWidget.item(ligne, 0).text()
        nom = self.ui.tableWidget.item(ligne, 1).text()
        email = self.ui.tableWidget.item(ligne, 2).text()
        tel = self.ui.tableWidget.item(ligne, 3).text()
        status = self.ui.tableWidget.item(ligne, 4).text()

        self.ui.lineEdit_IdClient.setText(id)
        self.ui.lineEdit_ModifNom.setText(nom)
        self.ui.lineEdit_ModEmail.setText(email)
        self.ui.lineEdit_ModTel.setText(tel)
        idx = self.ui.comboBoxStatus.findText(status)
        if idx>=0:
            self.ui.comboBoxStatus.setCurrentIndex(idx)