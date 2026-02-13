from dotenv import load_dotenv
import os
import mysql.connector as connector
import datetime

load_dotenv()

class DatabaseManager():
    def __init__(self):
        self.configuration={
            'host':os.getenv("DB_Host"),
            'user':os.getenv("DB_user"),
            'password': os.getenv("DB_PassWord"),
            'database' : os.getenv("DB_Name")
        }
        self.connexion = None

    def connecter(self):
        if self.connexion is None or not self.connexion.is_connected():
            try:
                self.connexion = connector.connect(**self.configuration)
            except Exception as e:
                print(f"Echec de connexion a la base des donnees: {e}")
        return self.connexion
    
    def fermer_connexion(self):
        if self.connexion and self.connexion.is_connected():
            self.connexion.close()

    def requetes_select(self, requette, params=None):
        self.connexion = self.connecter()
        resultats = None
        try:
            cursor = self.connexion.cursor(dictionary=True)
            cursor.execute(requette, params or ())
            resultats = cursor.fetchall()
        except Exception as e:
            print(f"Une erreur est survenu : {e}")
        finally:
            self.fermer_connexion() 
        return resultats
        

    def insert_update_delete(self, query, params=None, returnLastId=False):
        self.connexion = self.connecter()
        try:
            cursor = self.connexion.cursor()
            cursor.execute(query, params or ())
            self.connexion.commit()
            if returnLastId:
                return cursor.lastrowid
            print("Operation effectue avec succes")
        except Exception as e:
            self.connexion.rollback()
            print(f"Erreur {e}")
        finally:
            if cursor:
                cursor.close()
            self.fermer_connexion()

    def add_achat(self, clientID, montant):
        query = "INSERT INTO Achats (ClientID, Montant) VALUES (%s, %s);"
        self.insert_update_delete(query=query,params=(clientID,montant))

    def add_relation(self, parrainID, filleulID):
        query = "INSERT INTO Relations (parrainID, filleulID) VALUES (%s, %s);"
        self.insert_update_delete(query=query, params=(parrainID, filleulID))

    def add_client(self, ClientName, Email,Phone, parrainID=None):
            try:
                requete = "INSERT INTO Clients (ClientName, Email, Phone) VALUES (%s,%s,%s);"
                #inserer le client tout en recuperant son id pour la creation de la relation
                client_id = self.insert_update_delete(
                    query=requete,
                    params=(ClientName, Email, Phone),
                    returnLastId=True
                )
                # ajout de la reltion si il y en a
                # print("Insertion du client avec succes")
                if parrainID is not None and client_id is not None:
                    requette = "INSERT INTO Relations (parrainID,filleulID) VALUES (%s, %s);"
                    self.insert_update_delete(query=requette, params=(parrainID,client_id))
                    # print("insertion de la relation avec succes")
            except Exception as e:
                print(f"Erreur de l'ajout du client {e}")

    def update_client(self, id, ClientName, Email, Phone):
        message=""
        query = "UPDATE Clients SET ClientName= %s, Email=%s, Phone=%s WHERE ClientID=%s ;"
        try:
            self.insert_update_delete(query=query, params=(ClientName, Email, Phone, id))
            message = "Succes"
        except Exception as e :
            message = e
        return message
            
    def delete_client(self, id):
        query = "DELETE FROM Clients WHERE ClientID=%s ;"
        self.insert_update_delete(query=query, params=(id))

    def get_clients(self, all=True, ToSelect=None, exceptOne=False, idToExcept=None):
        if all:
            requete = "select * from Clients;"
        if ToSelect is not None :
            requete = f"select {ToSelect} from Clients"
        # Pour avoir tous les clients sauf un
        if exceptOne:
            requete += " whrere id !=%s"
            resultat = self.requetes_select(requette=requete, params=(idToExcept))
            return resultat
        
        resultat = self.requetes_select(requette=requete)
        return resultat
    
    def get_clients_plus_rentables(self):
        requette = "SELECT * FROM ClientsPlusRentable;"
        return self.requetes_select(requette=requette)
    
    def get_relations(self):
        query = "SELECT parrainID,filleulID FROM Relations;"
        resultats = self.requetes_select(requette=query)
        return resultats
    
    def get_tot_achats(self):
        query = "SELECT ClientID, SUM(Montant) AS total FROM Achats GROUP BY ClientID;"
        resultat = self.requetes_select(requette=query)
        achats_totaux = {}
        for ligne in resultat:
            achats_totaux[ligne["ClientID"]]=float(ligne["total"])
        return achats_totaux
    
    def get_achats_ClientName(self):
        query = "select Achats.ClientID, Clients.ClientName, Achats.Montant, Achats.DateAchat " \
        "from Achats inner join Clients where Clients.ClientID =Achats.ClientID;"
        resultat = self.requetes_select(requette=query)
        return resultat

    
    def get_tot_achat_par_client(self):
        query = "SELECT ClientID, SUM(Montant) AS total FROM Achats GROUP BY ClientID;"
        return self.requetes_select(requette=query)