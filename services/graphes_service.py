from database.database_manager import DatabaseManager
import networkx as nx
class GraphService:
    def __init__(self):
        self.db = DatabaseManager()
        
    
    def charger_les_donnees(self):
        self.relations = self.db.get_relations()
        self.achats = self.db.get_tot_achats()

    def construire_graphe(self, taux_direct=0.05):
        self.charger_les_donnees()
        graphe = {}
        for relation in self.relations:
            parrain = relation["parrainID"]
            filleul = relation["filleulID"]
            total = self.achats.get(filleul,0)
            poids = total*taux_direct
            # Ajout du parrain dans le graphe s'il n'y est pas
            if parrain not in graphe:
                graphe[parrain]=[]
            
            graphe[parrain].append((filleul, poids))

            # vu que le filleul doit etre aussi un sommet
            if filleul not in graphe:
                graphe[filleul] = []
        return graphe

    def construire_networkx_graph(self):
        NetGraph = nx.DiGraph()
        
        graphe = self.construire_graphe()
        for parrain, filleul in graphe.items():
            # Ajout du noeud parenet
            NetGraph.add_node(parrain)
            
            for child, poids in filleul:
                NetGraph.add_node(child)
                NetGraph.add_edge(parrain, child, weight= poids)
            
        return NetGraph
    