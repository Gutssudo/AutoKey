# main.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget
from lib.AFK.ongletAFK import OngletAFK  # Importer la classe OngletAFK depuis le fichier onglet_afk.py
from lib.Macro.ongletMacro import OngletMacro

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AutoKey")
        self.setGeometry(100, 100, 250, 300)
        self.setFixedWidth(320)
        # Création des onglets
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Ajout des onglets en utilisant la classe OngletAFK
        self.tab1 = OngletAFK()
        self.tab2 = OngletMacro()  # Vous pouvez utiliser une autre classe si nécessaire

        self.tabs.addTab(self.tab1, "Anti-AFK")
        self.tabs.addTab(self.tab2, "Macro")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
