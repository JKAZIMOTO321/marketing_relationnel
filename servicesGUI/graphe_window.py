from PyQt5.QtWidgets import QWidget, QVBoxLayout
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
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout(self.ui.widgetGraphe)
        layout.addWidget(self.canvas)
        self.ui.btnActualiser.clicked.connect(self.charger_graphe)
        self.charger_graphe()


    # def charger_graphe(self):
    #     self.figure.clear()
    #     if not self.grapheService.graphe:
    #         return
    #     NetGraph = self.grapheService.construire_networkx_graph()
    #     pos = nx.spring_layout(G=NetGraph, seed=42)
    #     weights = nx.get_edge_attributes(NetGraph, 'weight')
    #     nx.draw(
    #         G=NetGraph,
    #         pos=pos,
    #         with_labels=True,
    #         node_color='lightblue',
    #         node_size=2000,
    #         font_size=9,
    #         arrows=True
    #     )
    #     nx.draw_networkx_edge_labels(G=NetGraph, pos=pos, edge_labels=weights)
    #     self.canvas.draw

    def charger_graphe(self):
        self.figure.clear()
        NetGraph = self.grapheService.construire_networkx_graph()
        if NetGraph.number_of_nodes() == 0:
            return

        ax = self.figure.add_subplot(111)
        pos = nx.nx_pydot.graphviz_layout(NetGraph, prog="dot")
        nx.draw(
            NetGraph,
            pos,
            ax=ax,
            with_labels=True,
            node_color='lightblue',
            node_size=2000,
            font_size=9,
            arrows=True
        )
        # weights = nx.get_edge_attributes(NetGraph, 'weight')
        weights = nx.get_edge_attributes(NetGraph, 'weight')
        weights = {k: round(v, 1) for k, v in weights.items()}
        nx.draw_networkx_edge_labels(NetGraph, pos, edge_labels=weights, ax=ax)
        self.canvas.draw()