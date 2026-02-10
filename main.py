import sys
from PyQt5.QtWidgets import QApplication
from servicesGUI.main_window import MainWindow
from servicesGUI.relations_window import RelationsPage


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())