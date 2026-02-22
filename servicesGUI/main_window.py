from PyQt5.QtWidgets import QMainWindow, QApplication
from gui.ui_mainWindow import Ui_MainWindow
from .achat_window import AchatsPage
from .client_window import ClientPage
from .commission_window import CommissionPage
from .graphe_window import GraphePage
from .relations_window import RelationsPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #instanciation des pages
        self.fenetres = {
            "achats" : AchatsPage(),
            "clients" : ClientPage(mainWindow=self),
            "commissions": CommissionPage(mainWindow=self),
            "graphe" : GraphePage(),
            "relations" : RelationsPage(),
        }
        #Ajout de ces fenetre au stackedWidget du mainWindow pour permettre la navigation
        for fenetre in self.fenetres.values():
            self.ui.stackedWidget.addWidget(fenetre)

        #Mettre les pages dans le menu
        self.ui.actionAchats.triggered.connect(lambda: self.afficherFenetre("achats"))
        self.ui.actionClients.triggered.connect(lambda: self.afficherFenetre("clients"))
        self.ui.actionGraphe.triggered.connect(lambda : self.afficherFenetre("graphe"))
        self.ui.actionRelations.triggered.connect(lambda: self.afficherFenetre("relations"))

        self.afficherFenetre(nomFenetre="graphe")

    def afficherFenetre(self, nomFenetre):
        self.ui.stackedWidget.setCurrentWidget(self.fenetres[nomFenetre])


        

        