from PyQt5.QtWidgets import QWidget, QMessageBox
from gui.ui_clientWindow import Ui_Form
from services.client_services import ClientsService
from .utilitaires import demanderConfirmation, afficher_alerte, afficher_information

class ClientPage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.clientService = ClientsService()
        self.chargerParrainsComboBox(self.ui.comboBox_AddParrain)

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


        