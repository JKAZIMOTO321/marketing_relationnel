from database.database_manager import DatabaseManager

class ClientsService:
    def __init__(self):
        self.data = DatabaseManager()
        
    def recupererNomId(self, exceptOne=False, idToExcept=None):
        donnees = self.data.get_clients(
            all=False, 
            ToSelect="ClientID,ClientName",
            exceptOne=exceptOne, 
            idToExcept=idToExcept
        )
        return donnees
    
    def ajouterClient(self, Nom, Email, Phone, Parrain):
        try:
            self.data.add_client(ClientName=Nom, Email=Email, Phone=Phone, parrainID=Parrain)
            return True
        except Exception as e:
            return False
        
    def modifierClient(self, id, ClientName, Email, Phone):
        self.data.update_client(id=id, ClientName=ClientName, Email=Email, Phone=Phone)

    def supprimerClient(self, idClient):
        self.data.delete_client(id=idClient)


