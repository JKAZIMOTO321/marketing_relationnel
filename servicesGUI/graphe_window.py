from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from gui.ui_grapheWindow import Ui_Form
from services.graphes_service import GraphService
from .utilitaires import afficher_alerte
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class GraphePage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.grapheService = GraphService()
        # creation de la figure matplotlib
        self.figure = plt.figure(figsize=(12, 10))
        self.canvas = FigureCanvas(self.figure)

        # Scroll Area
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(False)  # IMPORTANT
        self.scrollArea.setWidget(self.canvas)

        layout = QVBoxLayout(self.ui.widgetGraphe)
        layout.addWidget(self.scrollArea)

        # Taille minimale du canvas (pour forcer le scroll si grand)
        self.canvas.setMinimumSize(1200, 900)
        self.ui.btnActualiser.clicked.connect(self.charger_graphe)
        self.charger_graphe()
        self.zoom_factor = 1.0
        self.ui.btnZoomPlus.clicked.connect(self.zoom_plus)
        self.ui.btnZoomMoins.clicked.connect(self.zoom_moins)

    def charger_graphe(self):
        self.figure.clear()
        NetGraph = self.grapheService.construire_networkx_graph()
        if NetGraph.number_of_nodes() == 0:
            return

        ax = self.figure.add_subplot(111)
        self.ax = ax
        try:
            # Trouver la racine (client qui n'a pas de parent)
            roots = [n for n, d in NetGraph.in_degree() if d == 0]

            if roots:
                root = roots[0]
            else:
                root = list(NetGraph.nodes())[0]

            pos = self.hierarchy_pos(NetGraph, root, width=10, vert_gap=2)
        except Exception:
            # Fallback if Graphviz/pydot is unavailable or layout fails.
            # pos = nx.spring_layout(NetGraph, seed=42)
            afficher_alerte("Erreur")
        self.pos = pos
        labels = {}
        for node in NetGraph.nodes():
            nom = self.grapheService.clientService.recupererNom(node)
            labels[node] = f"{node}\n{nom}"

        # 1. Dessiner les nœuds uniquement (sans labels pour l'instant)
        nx.draw_networkx_nodes(
            NetGraph,
            pos,
            ax=ax,
            node_color='#3498db', # Un bleu plus moderne
            node_size=1200,         # Taille réduite pour plus d'élégance
            edgecolors='white',    # Bordure blanche pour détacher le nœud
            linewidths=2
        )

        # 2. Dessiner les flèches (liens)
        nx.draw_networkx_edges(
            NetGraph,
            pos,
            ax=ax,
            arrowstyle='-|>',
            arrowsize=15,
            edge_color='gray',
            width=1.5
        )

        # 3. POSITIONNER LES LABELS (Le nom des clients)
        nx.draw_networkx_labels(
            NetGraph,
            pos,
            labels=labels,
            ax=ax,
            font_size=9,
            font_family='sans-serif',
            verticalalignment='center',
            horizontalalignment='center'
        )

        # 4. Afficher les poids (commissions) sur les arêtes
        weights = nx.get_edge_attributes(NetGraph, 'weight')
        weights = {k: f"{round(v, 1)}$" for k, v in weights.items()} # Ajout du symbole $
        nx.draw_networkx_edge_labels(
            NetGraph, 
            pos, 
            edge_labels=weights, 
            ax=ax, 
            font_color='red',
            font_size=10
        )
        # ID centré
        # id_labels = {node: str(node) for node in NetGraph.nodes()}

        # nx.draw_networkx_labels(
        #     NetGraph,
        #     pos,
        #     labels=id_labels,
        #     ax=ax,
        #     font_size=10,
        #     font_weight='bold',
        #     verticalalignment='center',
        #     horizontalalignment='center'
        # )

        # # Nom légèrement en dessous
        # name_pos = {k: (v[0], v[1] - 0.2) for k, v in pos.items()}
        # name_labels = {
        #     node: self.grapheService.clientService.recupererNom(node)
        #     for node in NetGraph.nodes()
        # }

        # nx.draw_networkx_labels(
        #     NetGraph,
        #     name_pos,
        #     labels=name_labels,
        #     ax=ax,
        #     font_size=8,
        #     verticalalignment='top',
        #     horizontalalignment='center'
        # )
        # Nettoyer les axes pour un look "pro"
        ax.set_axis_off()
        self.canvas.draw()

    def hierarchy_pos(self,G, root, width=1., vert_gap=1., vert_loc=0, xcenter=0.5):
        """
        Positionnement hiérarchique pour graphe orienté (arbre)
        """
        pos = {root: (xcenter, vert_loc)}
        children = list(G.successors(root))
        
        if len(children) != 0:
            dx = width / len(children)
            nextx = xcenter - width/2 - dx/2
            for child in children:
                nextx += dx
                pos.update(
                    self.hierarchy_pos(
                        G,
                        child,
                        width=dx,
                        vert_gap=vert_gap,
                        vert_loc=vert_loc - vert_gap,
                        xcenter=nextx
                    )
                )
        return pos
    
    def zoom_plus(self):
        pass

    def zoom_moins(self):
        pass