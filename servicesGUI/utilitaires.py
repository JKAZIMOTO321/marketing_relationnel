from PyQt5.QtWidgets import QMessageBox, QHeaderView,QTableWidgetItem
from PyQt5.QtCore import Qt
from services.client_services import ClientsService

cli = ClientsService()

def demanderConfirmation(fenetre,messageDemande):
    confirmation = QMessageBox.question(
        fenetre,
        "Confirmation",
        messageDemande,
        QMessageBox.Yes | QMessageBox.No
    )
    if confirmation == QMessageBox.Yes:
        return True
    else:
        return False
    
def afficher_alerte(message):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setWindowTitle("Attention")
    msg.setText(message)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()

def afficher_information(message):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setWindowTitle("Opération réussie")
    msg.setText(message)
    # msg.setInformativeText("Vous pouvez maintenant fermer l'application.")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()

def nettoyerLineEdit(listLineEdit):
    for el in listLineEdit:
        el.clear()

def ajusterColonnesDansTables(listTables):
    for table in listTables:
        table.horizontalHeader().setSectionResizeMode(
        QHeaderView.Stretch
        )

def chargerClientsDansComboBox(ComboBox, exceptOne=False, idToExcept=None):
        #depuis la BDD
        clients = None
        if exceptOne:
            clients = cli.recupererNomId(exceptUn=True, idToExcept=idToExcept)
        else :
            clients = cli.recupererNomId()

        if not clients:
            return

        for client in clients:
            client_id = client["ClientID"]
            clientNom = client["ClientName"]
            ComboBox.addItem(
                clientNom,
                client_id
            )

def _create_item(value):
        item = QTableWidgetItem(str(value))
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
        return item
