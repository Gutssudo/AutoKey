# onglet_afk.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget,
    QCheckBox, QButtonGroup, QLineEdit,QFileDialog, QTableWidgetItem
)
from PyQt5.QtGui import QIcon, QDoubleValidator

from pynput.keyboard import Listener, KeyCode, Controller, Key

from . import Table, RecFile, Translate
class OngletMacro(QWidget):
    def __init__(self):
        super().__init__()

        # Layout principal vertical pour l'onglet
        self.mainLayout = QVBoxLayout()

        # Layout horizontal pour les boutons
        self.buttonLayout = QHBoxLayout()
        self.RECbutton = QPushButton("Rec")
        self.buttonLayout.addWidget(self.RECbutton)
        self.RECbutton.clicked.connect(self.addKey)
        self.RECIcon = QIcon("ico/record.png")
        self.RECbutton.setIcon(self.RECIcon)


        self.LOADbutton = QPushButton("Load")
        self.buttonLayout.addWidget(self.LOADbutton)
        self.LOADbutton.clicked.connect(self.loadFile)
        self.LOADIcon = QIcon("ico/loadFile.png")
        self.LOADbutton.setIcon(self.LOADIcon)

        self.RESETbutton = QPushButton("Reset")
        self.buttonLayout.addWidget(self.RESETbutton)
        self.RESETbutton.clicked.connect(self.Reset)
        self.RESETIcon = QIcon("ico/load.png")
        self.RESETbutton.setIcon(self.RESETIcon)

        # Ajout du layout des boutons au layout principal
        self.mainLayout.addLayout(self.buttonLayout)
        self.HLayout = QHBoxLayout()
        # Liste d'éléments
        listKey = []
        self.table = Table.TableWidget(actions=listKey)
        self.table.setFixedWidth(217)
        # self.table.set(217,150)

        self.HLayout.addWidget(self.table)
        self.VLayout = QVBoxLayout()
        self.Delaybutton = QPushButton("add Delay")
        self.Delaybutton.clicked.connect(self.table.addDelayItem)


        self.StartKeyBut = QPushButton("select\n Start Key...")
        self.StartKeyBut.clicked.connect(self.StartKey)

        self.VLayout.addWidget(self.Delaybutton)
        self.VLayout.addWidget(self.StartKeyBut)


        self.HLayout.addLayout(self.VLayout)
        self.mainLayout.addLayout(self.HLayout)


        # Ajouter un espace entre le layout et le bouton Play


        self.PSLayout = QHBoxLayout()
        
        self.SaveButton = QPushButton("Save")
        self.PSLayout.addWidget(self.SaveButton)
        # self.SaveButton.clicked.connect(self.save_yaml)
        self.SaveIcon = QIcon("ico/save.png")
        self.SaveButton.setIcon(self.SaveIcon)

        # Ajouter un bouton Play à la fin du layout principal
        self.PlayButton = QPushButton("Play")
        # self.PlayButton.clicked.connect(self.Play)
        self.PlayIcon = QIcon("ico/play.png")
        self.PlayButton.setIcon(self.PlayIcon)

        self.PSLayout.addWidget(self.PlayButton)

        self.mainLayout.addLayout(self.PSLayout)
        # Appliquer le layout principal à l'onglet
        self.setLayout(self.mainLayout) 

    def addKey(self):
        key = str(RecFile.RecFunc())
        # self.list.addItem(str(key))
        print(f'key:{key}')

        # rowPosition = self.table.rowCount()
        self.table.add_list_to_row(0, [key])


    def addDelay(self):
        key = str(RecFile.RecFunc())
        rowPosition = self.table.rowCount()
        self.table.insertRow(rowPosition)
        self.table.setItem(rowPosition,0,QTableWidgetItem(key))

    def Reset(self):
        self.table.RemoveAllRow()
        self.StartKeyBut.setText("select\n Start Key...")

    def open_file_dialog(self):
        # Ouvrir la boîte de dialogue de sélection de fichiers
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Sélectionner un Fichier", "",
                                                   "Tous les fichiers (*);;Fichier xml (*.xml);;Fichier txt (*.txt)", options=options)
        file_path=(str(file_name))
        return file_name, file_path

    def loadFile(self):
        keys =[]
        file,file_path = self.open_file_dialog()
        print(file_path)
        with open(file, 'r') as file:
    # Lire toutes les lignes dans une liste
            lignes = file.readlines()

        # for ligne in lignes:
        #     print(ligne)
        if file_path.endswith('.txt'):
            for ligne in lignes:
                ligne = ligne.replace('e=', '').replace('}','').replace('{','')
                keys.append(ligne)
            translatedFile = Translate.TradPyMgp(keys,'Code','pynput_key')
            print(translatedFile)
            translatedFile = [item for item in translatedFile if item != ['', '']]

            for row, (key, value) in enumerate(translatedFile):
                print(row, key)
            print(translatedFile)
            self.table.loadFileTable(row, translatedFile)
                # self.table.setItem(row, 1, QTableWidgetItem(value))
            # self.table.setItem(row, 0, QTableWidgetItem(str(translatedFile[0])))



    def StartKey(self):
        StartKey = RecFile.RecFunc()
        self.StartKeyBut.setText(str(StartKey))