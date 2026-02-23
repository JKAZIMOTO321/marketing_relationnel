from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QMessageBox, QTableWidgetItem
from gui.ui_clientWindow import Ui_Form
from services.client_services import ClientsService
from .commission_window import CommissionPage
from .utilitaires import (demanderConfirmation, afficher_alerte, 
                          afficher_information, nettoyerLineEdit, 
                          ajusterColonnesDansTables, chargerClientsDansComboBox)

class ClientPage(QWidget):
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
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
        self.ui.btnModifier.clicked.connect(self.modifierClient)
        self.ui.btnSupprimer.clicked.connect(self.supprimerClient)
        self.ui.btnCommissions.clicked.connect(self.voirCommission)

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
                self.chargerDonneesDansTable()
            if not ajout:
                afficher_alerte(message="Echec de l'enregistrement")
            nettoyerLineEdit(self.elementsAdd)
        # actualisation des donnees dans achatsWindow
        self.actualiserAchats()

    def chargerParrainsComboBox(self, ComboBox):
        ComboBox.clear()
        ComboBox.addItem("Aucun Parrain", None)
        #depuis la BDD
        chargerClientsDansComboBox(ComboBox=ComboBox)

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
        id = self.ui.tableWidget.item(ligne, 0).text()
        nom = self.ui.tableWidget.item(ligne, 1).text()
        email = self.ui.tableWidget.item(ligne, 2).text()
        tel = self.ui.tableWidget.item(ligne, 3).text()

        self.ui.lineEdit_IdClient.setText(id)
        self.ui.lineEdit_ModifNom.setText(nom)
        self.ui.lineEdit_ModEmail.setText(email)
        self.ui.lineEdit_ModTel.setText(tel)

    def modifierClient(self):
        id = int(self.ui.lineEdit_IdClient.text())
        nom = self.ui.lineEdit_ModifNom.text()
        email = self.ui.lineEdit_ModEmail.text()
        tel = self.ui.lineEdit_ModTel.text()
        confirm = demanderConfirmation(fenetre=self, 
                                           messageDemande="Voulez vous vraiment modifier")
        if confirm:
            try:
                action =self.clientService.modifierClient(id=id, ClientName=nom, Email=email, Phone=tel)
                afficher_information(message="Succes")
            except Exception as e:
                afficher_alerte(message=f"Erreur : {e}")
        self.actualiserAchats()

    def supprimerClient(self):
        confirm = demanderConfirmation(fenetre=self, 
            messageDemande="Voulez vous vraiment supprimer ?")
        if confirm:
            confirm2 = demanderConfirmation(fenetre=self, 
            messageDemande="Voulez vous vraiment le supprimer ?")
            if confirm2:
                try:
                    id= int(self.ui.lineEdit_IdClient.text())
                    self.clientService.supprimerClient(idClient=id)
                    afficher_information(message="Suppression reussie")
                except Exception as e:
                    afficher_alerte(message=f"Echec de suppression : {e}")
        self.actualiserAchats()

    def voirCommission(self):
        try:
            idClient = int(self.ui.lineEdit_IdClient.text())
            commissionWindow = self.mainWindow.fenetres["commissions"]
            #on passe l'id en parametre
            commissionWindow.idClient=idClient
            commissionWindow.charger_commissions()
            self.mainWindow.ui.stackedWidget.setCurrentWidget(commissionWindow)
        except:
            afficher_alerte(message="Veuillez d'abord selectionner un client")

            
    def actualiserAchats(self):
        # actualisation des donnees dans achatsWindow
        achatWindow = self.mainWindow.fenetres["achats"]
        achatWindow.actualiserData()
        
        