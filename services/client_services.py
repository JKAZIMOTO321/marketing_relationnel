from database.database_manager import DatabaseManager

class ClientsService:
    def __init__(self):
        self.data = DatabaseManager()
        
    def recupererNomId(self, exceptUn=False, idToExcept=None):
        donnees = self.data.get_clients(
            all=False, 
            ToSelect="ClientID,ClientName",
            exceptOne=exceptUn, 
            idToExcept=idToExcept
        )
        return donnees
    
    def recupererNom(self, idClient):
        nomDict = self.data.get_clients(
            all=False,
            ToSelect="ClientName",
            oneSelect=idClient
        )
        nomText = nomDict[0]["ClientName"]
        return nomText
    
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


