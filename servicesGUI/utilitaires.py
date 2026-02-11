from PyQt5.QtWidgets import QMessageBox, QHeaderView

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