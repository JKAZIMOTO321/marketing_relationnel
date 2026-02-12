from database.database_manager import DatabaseManager

class AchatsServices:
    def __init__(self):
        self.db = DatabaseManager()

    def enregistrerAchat(self, idClient, Montant):
        self.db.add_achat(clientID=idClient, montant=Montant)
