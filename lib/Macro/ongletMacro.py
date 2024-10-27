import os
import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QTableWidgetItem, QLineEdit, QComboBox, QMainWindow
)
from PyQt5.QtGui import QIcon
from pynput.keyboard import Controller
import threading
from . import Table, RecFile, Translate, PlayFile, SaveFile

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class OngletMacro(QWidget):
    def __init__(self):
        super().__init__()
        self.stopbool = True
        self.mainLayout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout()

        self.RECbutton = QPushButton("Rec")
        self.buttonLayout.addWidget(self.RECbutton)
        self.RECbutton.clicked.connect(self.addKey)
        self.RECIcon = QIcon(resource_path("ico/record.png"))
        self.RECbutton.setIcon(self.RECIcon)

        self.LOADbutton = QPushButton("Load")
        self.buttonLayout.addWidget(self.LOADbutton)
        self.LOADbutton.clicked.connect(self.loadFile)
        self.LOADIcon = QIcon(resource_path("ico/loadFile.png"))
        self.LOADbutton.setIcon(self.LOADIcon)

        self.RESETbutton = QPushButton("Reset")
        self.buttonLayout.addWidget(self.RESETbutton)
        self.RESETbutton.clicked.connect(self.Reset)
        self.RESETIcon = QIcon(resource_path("ico/load.png"))
        self.RESETbutton.setIcon(self.RESETIcon)

        self.mainLayout.addLayout(self.buttonLayout)
        self.HLayout = QHBoxLayout()
        self.table = Table.TableWidget()
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
        self.mainLayout.addStretch()

        self.SaveButton = QPushButton("Save")
        self.mainLayout.addWidget(self.SaveButton)
        self.SaveButton.clicked.connect(self.Save)
        self.SaveIcon = QIcon(resource_path("ico/save.png"))
        self.SaveButton.setIcon(self.SaveIcon)

        self.PSLayout = QHBoxLayout()
        self.PlayButton = QPushButton("Play")
        self.PlayButton.clicked.connect(self.Play)
        self.PlayIcon = QIcon(resource_path("ico/play.png"))
        self.PlayButton.setIcon(self.PlayIcon)

        self.PSLayout.addWidget(self.PlayButton)

        self.StopButton = QPushButton("Stop")
        self.StopButton.clicked.connect(self.Stop)
        self.StopIcon = QIcon(resource_path("ico/stop.png"))
        self.StopButton.setIcon(self.StopIcon)

        self.PSLayout.addWidget(self.StopButton)
        self.mainLayout.addLayout(self.PSLayout)
        self.setLayout(self.mainLayout)

    def addKey(self):
        key = str(RecFile.RecFunc())
        print(f'key:{key}')
        self.table.addActions(0, key)
        self.table.Colum1Row(self.table.rowCount() - 1)

    def Reset(self):
        self.table.RemoveAllRow()
        self.StartKeyBut.setText("select\n Start Key...")

    def open_file_dialog(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Sélectionner un Fichier", "",
                                                   "Tous les fichiers (*);;Fichier xml (*.xml);;Fichier txt (*.txt)", options=options)
        return file_name

    def loadFile(self):
        self.Reset()
        keys = []
        try:
            file = self.open_file_dialog()
            if file:
                file_path = os.path.abspath(str(file))
                if file_path.endswith('.txt'):
                    yaml = False
                    with open(file_path, 'r') as file:
                        lignes = file.readlines()
                    for ligne in lignes:
                        ligne = ligne.replace('e=', '').replace('}', '').replace('{', '')
                        keys.append(ligne)
                    translatedFile, suffix, startKey = Translate.TradPyMgp(keys, 'Code', 'pynput_key')
                elif file_path.endswith('.yaml'):
                    yaml = True
                    startKey, translatedFile = Translate.TradYamlPy(file_path)
                if startKey is not None:
                    self.StartKeyBut.setText(startKey.lower() if len(startKey) == 1 else startKey)
                translatedFile = [item for item in translatedFile if item != ['', '']]
                self.table.loadFileTable(translatedFile, yaml)
        except Exception as e:
            print(f"Erreur : {e}")

    def StartKey(self):
        StartKey = RecFile.RecFunc()
        self.StartKeyBut.setText(str(StartKey))

    def Play(self):
        self.Stop()
        actions = self.getTableContent()
        startKey = self.StartKeyBut.text()
        print(startKey)
        self.playobj = PlayFile.PlayFile(actions, startKey)
        self.stopbool = False

    def getTableContent(self):
        content = []
        rowCount = self.table.rowCount()
        columnCount = self.table.columnCount()
        for row in range(rowCount):
            rowData = []
            for column in range(columnCount):
                item = self.table.item(row, column)
                if column == 0:
                    rowData.append(item.text())
                else:
                    item = self.table.cellWidget(row, column)       
                    if isinstance(item, QLineEdit):
                        rowData.append(item.text())
                    elif isinstance(item, QComboBox):
                        rowData.append(item.currentText())
            content.append(rowData)

        formattedContent = [[row[0], row[1]] for row in content]
        return formattedContent

    def Stop(self):
        if self.stopbool is not True:             
            self.playobj.killProcess()
            print('Process kill')

    def Save(self):
        actions = self.getTableContent()
        startKey = self.StartKeyBut.text()
        SaveFile.save(self, startKey, actions)
