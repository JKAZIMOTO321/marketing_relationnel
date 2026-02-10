from PyQt5.QtWidgets import QMessageBox

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