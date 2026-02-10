from database.database_manager import DatabaseManager

class ClientsService:
    def __init__(self):
        self.data = DatabaseManager()
        
    def recupererNomId(self):
        donnees = self.data.get_clients(all=False, ToSelect="ClientID,ClientName")
        return donnees
    
    def ajouterClient(self, Nom, Email, Phone, Parrain):
        try:
            self.data.add_client(ClientName=Nom, Email=Email, Phone=Phone, parrainID=Parrain)
            return True
        except Exception as e:
            return False
