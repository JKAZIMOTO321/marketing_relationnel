from PyQt5.QtWidgets import QWidget
from gui.ui_clientWindow import Ui_Form
from services.client_services import ClientsService

class ClientPage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.clientService = ClientsService()
        self.chargerParrainsComboBox(self.ui.comboBox_AddParrain)


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

        