from database import DatabaseManager as db
class GraphService:
    def __init__(self):
        self.relations = db.get_relations()
        self.achats = db.get_tot_achats()
        self.graphe = self.construire_graphe()
    
    def construire_graphe(self, taux_direct=0.05):
        graphe = {}
        for relation in self.relations:
            parrain = relation["parrainID"]
            filleul = relation["filleulID"]
            total = self.achats.get(filleul,0)
            poids = total*taux_direct
            # Ajout du parrain dans le graphe s'il n'y est pas
            if parrain not in self.graphe:
                graphe[parrain]=[]
            
            graphe[parrain].append((filleul, poids))

            # vu que le filleul doit etre aussi un sommet
            if filleul not in graphe:
                graphe[filleul] = []
        return graphe

    