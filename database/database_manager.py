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
        try:
            cursor = self.connexion.cursor(dictionary=True)
            cursor.execute(requette, params or ())
            resultats = cursor.fetchall()
        except Exception as e:
            print(f"Une erreur est survenu : {e}")
        finally:
            self.fermer_connexion() 

    def insert_update_delete(self, query, params=None, returnLastId=False):
        self.connexion = self.connecter()
        try:
            cursor = self.connexion.cursor()
            cursor.execute(query, params or ())
            self.connexion.commit()
            self.connexion.close()
            if returnLastId:
                return cursor.lastrowid()
        except Exception as e:
            self.connexion.rollback()
            print(f"Erreur {e}")
        finally:
            self.fermer_connexion()
    
    def get_clients(self):
        requete = "SELECT * FROM Clients"
        return self.requetes_select(requette=requete)
        
    def add_client(self, ClientName, Email,Phone, parrainID=None):
            try:
                requete = "INSERT INTO Clients (ClientName, Email, Phone) VALUES (%s,%s,%s);"
                # recuperation l'id du client pour pouvoir creer la relation si il y en a
                client_id = self.insert_update_delete(query=requete,params=(ClientName, Email, Phone),returnLastId=True)
                # ajout de la reltion si il y en a
                if parrainID is not None:
                    requette = "INSERT INTO Relations (parrainID,filleulID) VALUES (%s, %s,);"
                    self.insert_update_delete(requette, (parrainID,client_id))
            except Exception as e:
                print(f"Erreur de l'ajout du client {e}")

    def get_clients_plus_rentables(self):
        requette = "SELECT * FROM ClientsPlusRentable;"
        return self.requetes_select(requette=requette)
    
    def get_relations(self):
        requette = "SELECT parrainID,filleulID FROM Relations;"
        return self.requetes_select(requette=requette)
        

