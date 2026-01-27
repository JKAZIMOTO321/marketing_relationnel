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

            
    
    def get_clients(self):
        conn = self.connecter()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Clients")
            result = cursor.fetchall()
            conn.close()
            return result
        
    def add_client(self, ClientName, Email,Phone, parrainID=None):
        self.connexion = self.connecter()
        if self.connexion:
            try:
                cursor = self.connexion.cursor(dictionary=True)
                requete = "INSERT INTO Clients (ClientName, Email, Phone) VALUES (%s,%s,%s);"
                cursor.execute(requete,(ClientName, Email, Phone))
                # recuperation l'id du client pour pouvoir creer la relation si il y en a
                client_id = cursor.lastrowid()
                # ajout de la reltion si il y en a
                if parrainID is not None:
                    requette = "INSERT INTO Relations (parrainID,filleulID) VALUES (%s, %s,);"
                    cursor.execute(requete, (parrainID,client_id))
                self.connexion.commit()
                print("Ajouts reussi")
                self.fermer_connexion()
            except Exception as e:
                self.connexion.rollback()
                print(f"Erreur de l'ajout du client {e}")

    def get_clients_plus_rentables(self):
        self.connexion = self.connecter()
        if self.connexion:
            try:
                cursor = self.connexion.cursor()
                requette = "SELECT * FROM ClientsPlusRentable;"
                cursor.execute(requette)
                resultats = cursor.fetchall()
            except Exception as e:
                print(f"Erreur lors de la recherche {e}")
                resultats = None
        return resultats
    
    def get_relations(self):
        pass
        

