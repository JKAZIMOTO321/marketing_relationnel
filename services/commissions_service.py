from graphes_service import GraphService

class CommissionService:
    def __init__(self):
        self.graph_service = GraphService()
        self.graphe = self.graph_service.graphe
        self.achats_totaux = self.graph_service.achats

    def dfs_commission(self, graphe, achats_totaux, client_courant,niveau, visited):
        commission = 0
        visited.add(client_courant)

        taux = 0.05 if niveau == 1 else 0.01

