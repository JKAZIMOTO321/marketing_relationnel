from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from gui.ui_grapheWindow import Ui_Form
from services.graphes_service import GraphService
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

    def charger_graphe(self):
        self.figure.clear()
        NetGraph = self.grapheService.construire_networkx_graph()
        if NetGraph.number_of_nodes() == 0:
            return

        ax = self.figure.add_subplot(111)
        try:
            # NetworkX >= 3.0 no longer supports the `args` parameter.
            # Set Graphviz spacing through graph attributes instead.
            layout_graph = NetGraph.copy()
            layout_graph.graph["ranksep"] = "1.5"
            layout_graph.graph["nodesep"] = "1"
            pos = nx.nx_pydot.graphviz_layout(layout_graph, prog="dot")
        except Exception:
            # Fallback if Graphviz/pydot is unavailable or layout fails.
            pos = nx.spring_layout(NetGraph, seed=42)

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
            node_size=600,         # Taille réduite pour plus d'élégance
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
        # On crée un décalage vers le haut pour que le texte ne soit pas SUR le nœud
        label_pos = {k: [v[0], v[1] + 0.15] for k, v in pos.items()} 
        
        nx.draw_networkx_labels(
            NetGraph,
            label_pos,
            labels=labels,
            ax=ax,
            font_size=10,
            # font_weight='bold',
            font_family='sans-serif'
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

        # Nettoyer les axes pour un look "pro"
        ax.set_axis_off()
        self.canvas.draw()