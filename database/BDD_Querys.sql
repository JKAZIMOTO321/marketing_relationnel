create database if not exists DB_Marketing_Relationnel_Algo2;

use DB_Marketing_Relationnel_Algo2;
CREATE TABLE IF NOT EXISTS Clients (
    ClientID INT AUTO_INCREMENT PRIMARY KEY,
    ClientName VARCHAR(100) NOT NULL,
    Email VARCHAR(150) NOT NULL UNIQUE,
    Phone VARCHAR(20) UNIQUE,
    DateInscription datetime DEFAULT current_timestamp,
    Statut VARCHAR(20) DEFAULT 'ACTIF'
);

-- La table Relations
CREATE TABLE IF NOT EXISTS Relations (
    idRelation INT AUTO_INCREMENT PRIMARY KEY,
    parrainID INT NULL,
    filleulID INT NOT NULL UNIQUE,
    DateRelation DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_parrain
        FOREIGN KEY (parrainID) REFERENCES Clients(ClientID)
        ON DELETE SET NULL,

    CONSTRAINT fk_filleul
        FOREIGN KEY (filleulID) REFERENCES Clients(ClientID)
        ON DELETE CASCADE
) ENGINE=InnoDB;

-- Trigger pour la logique que un client ne peut pas etre parrain de lui meme
CREATE TRIGGER trg_check_parrain_filleul
BEFORE INSERT ON Relations
FOR EACH ROW
BEGIN
    IF NEW.parrainID = NEW.filleulID THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Un client ne peut pas être son propre parrain';
    END IF;
END;

-- Creation de la table achats
CREATE TABLE IF NOT EXISTS Achats (
    idAchat INT AUTO_INCREMENT PRIMARY KEY,
    ClientID INT NOT NULL,
    DateAchat datetime DEFAULT current_timestamp,
    Montant DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (ClientID) REFERENCES Clients(ClientID)
        ON DELETE CASCADE
) ENGINE=InnoDB;
-- trigger pour verifier si le montant est superieur a 0 
CREATE TRIGGER trg_check_montant_achat
BEFORE INSERT ON Achats
FOR EACH ROW
BEGIN
    IF NEW.Montant <= 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Le montant doit être supérieur à 0';
    END IF;
END;

-- La vue des clients les plus rentables
CREATE OR REPLACE VIEW ClientsPlusRentable AS
SELECT 
    Clients.ClientName, 
    SUM(Achats.Montant) AS TotalAchats
FROM Clients
JOIN Achats ON Clients.ClientID = Achats.ClientID
GROUP BY Clients.ClientID, Clients.ClientName
ORDER BY TotalAchats DESC;