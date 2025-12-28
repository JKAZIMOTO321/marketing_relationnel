import sqlite3

class ActionsLieeALaDB():
    def __init__(self):

        #Chemin vers la base des donnees
        self.db_path = "data/database.db"
        
        pass

    def recuperer_tous_les_clients(db_path):
        db_connexion = sqlite3.connect(db_path)
        cursor = db_connexion.cursor()

        #requette pour prende les clients dans la base des donnees
        requete = """
            SELECT * FROM Clients
        """
        pass
    
    def recuperer_tous_les_relations(de_path):
        pass

    def recuperer_client_plus_rentable(db_path, lim_Max):
        pass

    def generer_graphe_depuis_db(db_path):
        pass