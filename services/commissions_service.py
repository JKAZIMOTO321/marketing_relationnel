from services import GraphService
from .client_services import ClientsService

class CommissionService:
    def __init__(self):
        self.graph_service = GraphService()
        self.clientsS = ClientsService()
        self.graphe = self.graph_service.construire_graphe()
        self.achats_totaux = self.graph_service.achats
        
    
    def dfs_commission(self, client_courant, niveau, visited):
        visited.add(client_courant)

        commissions_directes = []
        commissions_indirectes = []

        for filleul, _ in self.graphe.get(client_courant, []):
            if filleul not in visited:

                total_achat = self.achats_totaux.get(filleul, 0)

                if niveau == 1:
                    taux = 0.05
                    commission = total_achat * taux
                    commissions_directes.append((filleul, total_achat, commission))
                else:
                    taux = 0.01
                    commission = total_achat * taux
                    commissions_indirectes.append((filleul, total_achat, commission))

                # récursion
                d, i = self.dfs_commission(filleul, niveau + 1, visited)
                commissions_directes += d
                commissions_indirectes += i

        return commissions_directes, commissions_indirectes
    
    def get_commissions_details(self, parrainID):
        visited = set()
        return self.dfs_commission(parrainID, 1, visited)
    
    def get_nomClient(self,idClient):
        nom = self.clientsS.recupererNom(idClient=idClient)
        return nom
