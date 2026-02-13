from database.database_manager import DatabaseManager
from .graphes_service import GraphService

class RelationService:
    def __init__(self):
        self.db = DatabaseManager()
        self.grapheService = GraphService()

    def get_data_tableau(self):
        data = self.db.get_relations_ClientName()
        return data
    
    def relationCreeraitCycle(self, parrainID, filleulID):
        graphe = self.grapheService.construire_graphe()
        visited = set()

        def dfs(noeud):
            if noeud == parrainID:
                return True
            visited.add(noeud)

            for voisin, _ in graphe.get(noeud, []):
                if voisin not in visited:
                    if dfs(voisin):
                        return True
            return False

        return dfs(filleulID)