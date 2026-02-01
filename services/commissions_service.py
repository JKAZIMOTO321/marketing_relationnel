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
        for filleul, _ in graphe.get(client_courant,[]):
            if filleul not in visited:
                total_achat = achats_totaux.get(filleul,0)
                gain = total_achat*taux
                commission += gain

                # recursivité
                commission += self.dfs_commission(
                    graphe,
                    achats_totaux,
                    filleul,
                    niveau+1,
                    visited
                )
        return commission

