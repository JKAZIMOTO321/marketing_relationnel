class GraphService:
    def __init__(self, relations, achats):
        self.relations = relations
        self.achats = achats
        self.graphe = {}
    
    def construire_graphe(self, taux_direct=0.05):
        relations = self.get_relations()
        achats_totaux = self.get_tot_achats()
        graphe = {}

        for relation in relations:
            parrain = relation["parrainID"]
            filleul = relation["filleulID"]
            total = achats_totaux.get(filleul,0)
            poids = total*taux_direct
            # Ajout du parrain dans le graphe s'il n'y est pas
            if parrain not in graphe:
                graphe[parrain]=[]
            graphe[parrain].append((filleul, poids))

            # vu que le filleul doit etre aussi un sommet
            if filleul not in graphe:
                graphe[filleul] = []
        return graphe

    