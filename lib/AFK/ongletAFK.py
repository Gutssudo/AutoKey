# onglet_afk.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget,
    QCheckBox, QButtonGroup, QLineEdit,QFileDialog
)
from PyQt5.QtGui import QIcon, QDoubleValidator

from . import RecFile, LoadFile, SaveFile, PlayFile
from pynput.keyboard import Listener, KeyCode, Controller, Key
class OngletAFK(QWidget):
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

        # Liste d'éléments
        self.list = QListWidget()
        self.list.addItems([])
        self.mainLayout.addWidget(self.list)

        # Créer un layout horizontal pour séparer Delay et Time
        self.topLayout = QHBoxLayout()

        # Layout pour Time (à gauche)
        self.timeLayout = QVBoxLayout()
        self.TimeLabel = QLabel("Time:")
        self.timeLayout.addWidget(self.TimeLabel)

        # Layout horizontal pour la case "Fix" avec un champ de saisie après Time
        self.timeFixLayout = QHBoxLayout()
        self.TimeFix = QCheckBox("Fix")
        self.timeFixInput = QLineEdit()
        self.timeFixInput.setPlaceholderText("time (s)")
        self.timeFixInput.setValidator(QDoubleValidator(0.99, 99.99, 2))


        self.timeFixLayout.addWidget(self.TimeFix)
        self.timeFixLayout.addWidget(self.timeFixInput)

        # Layout pour la case "Inf" après Time
        self.timeInfLayout = QHBoxLayout()
        self.TimeInf = QCheckBox("Inf")
        self.timeInfLayout.addWidget(self.TimeInf)

        # Ajouter les nouveaux éléments à la timeLayout
        self.timeLayout.addLayout(self.timeFixLayout)
        self.timeLayout.addLayout(self.timeInfLayout)

        self.buttonGroupTime = QButtonGroup()
        self.buttonGroupTime.addButton(self.TimeInf)
        self.buttonGroupTime.addButton(self.TimeFix)
        self.buttonGroupTime.setExclusive(True)
        # Ajouter le layout Time à gauche
        self.topLayout.addLayout(self.timeLayout)

        # Créer un layout pour Delay (à droite)
        self.DelayLayout = QVBoxLayout()
        self.DelayLabel = QLabel("Delay :")
        self.DelayLayout.addWidget(self.DelayLabel)

        # Layout horizontal pour la case "Fix" avec un champ de saisie
        self.fixLayout = QHBoxLayout()
        self.DelayFix = QCheckBox("Fix")
        self.fixInput = QLineEdit()
        self.fixInput.setValidator(QDoubleValidator(0.99, 99.99, 2))
        self.fixInput.setPlaceholderText("delay (s)")

        # Ajouter la case "Fix" et le champ de saisie au layout horizontal
        self.fixLayout.addWidget(self.DelayFix)
        self.fixLayout.addWidget(self.fixInput)

        # Ajouter le layout horizontal au layout Delay
        self.DelayLayout.addLayout(self.fixLayout)

        # Layout horizontal pour la case "Entre" avec deux champs de saisie
        self.entreLayout = QHBoxLayout()
        self.DelayAlea = QCheckBox("Entre")
        self.entreInput1 = QLineEdit()
        self.entreInput1.setPlaceholderText("min (s)")
        self.entreInput2 = QLineEdit()
        self.entreInput2.setPlaceholderText("max (s)")
        self.entreInput1.setValidator(QDoubleValidator(0.99, 99.99, 2))
        self.entreInput2.setValidator(QDoubleValidator(0.99, 99.99, 2))



        # Ajouter les widgets au layout horizontal pour "Entre"
        self.entreLayout.addWidget(self.DelayAlea)
        self.entreLayout.addWidget(self.entreInput1)
        self.entreLayout.addWidget(QLabel("et"))
        self.entreLayout.addWidget(self.entreInput2)

        # Ajouter le layout horizontal "Entre" au layout Delay
        self.DelayLayout.addLayout(self.entreLayout)

        # Créer un QButtonGroup pour les cases à cocher
        self.buttonGroupDelay = QButtonGroup()
        self.buttonGroupDelay.addButton(self.DelayFix)
        self.buttonGroupDelay.addButton(self.DelayAlea)
        self.buttonGroupDelay.setExclusive(True)  # Assurer que les cases sont exclusives

        # Ajouter le layout Delay à droite
        self.topLayout.addLayout(self.DelayLayout)

        # Ajouter le topLayout au layout principal
        self.mainLayout.addLayout(self.topLayout)

        # Ajouter un espace entre le layout et le bouton Play
        self.mainLayout.addStretch()

        self.SaveButton = QPushButton("Save")
        self.mainLayout.addWidget(self.SaveButton)
        self.SaveButton.clicked.connect(self.save_yaml)
        self.SaveIcon = QIcon("ico/save.png")
        self.SaveButton.setIcon(self.SaveIcon)

        self.PSLayout = QHBoxLayout()
        # Ajouter un bouton Play à la fin du layout principal
        self.PlayButton = QPushButton("Play")
        self.PlayButton.clicked.connect(self.Play)
        self.PlayIcon = QIcon("ico/play.png")
        self.PlayButton.setIcon(self.PlayIcon)

        self.PSLayout.addWidget(self.PlayButton)

        self.StopButton = QPushButton("Stop")
        self.StopButton.clicked.connect(self.Stop)
        self.StopIcon = QIcon("ico/stop.png")
        self.StopButton.setIcon(self.StopIcon)

        self.PSLayout.addWidget(self.StopButton)


        self.mainLayout.addLayout(self.PSLayout)
        # Appliquer le layout principal à l'onglet
        self.setLayout(self.mainLayout)

    def open_file_dialog(self):
        # Ouvrir la boîte de dialogue de sélection de fichiers
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Sélectionner un Fichier", "",
                                                   "Tous les fichiers (*);;Fichier yaml (*.yaml)", options=options)
        return file_name

    def Reset(self):
        self.list.clear()
        self.timeFixInput.setPlaceholderText('time (s)')
        self.timeFixInput.setText('')
        self.fixInput.setPlaceholderText('delay (s)')
        self.fixInput.setText('')

        self.entreInput1.setPlaceholderText('min (s)')
        self.entreInput1.setText('')

        self.entreInput2.setPlaceholderText('max (s)')
        self.entreInput2.setText('')


    def addKey(self):
        key = RecFile.RecFunc()
        self.list.addItem(str(key))

    def save_yaml(self):
        # self.keys = self.list.text()
        self.keys = [self.list.item(i).text() for i in range(self.list.count())]

        if self.DelayFix.isChecked():
            self.delay = self.fixInput.text()
        else :
            self.delay = [self.entreInput1.text(),self.entreInput2.text()]
        if self.TimeFix.isChecked():
            self.time = self.timeFixInput.text()
        else :
            self.time = 'inf'
        SaveFile.save(self, self.keys, self.delay, self.time)

    def loadFile(self):
        self.Reset()

        file = self.open_file_dialog()
        self.time, self.delay, self.keys = LoadFile.LoadFunc(file)
        if self.time != 'inf':
            self.TimeFix.setChecked(True)
            self.timeFixInput.setText(self.time)
        else :
            self.TimeInf.setChecked(True)
        if isinstance(self.delay, list):
            self.DelayAlea.setChecked(True)
            self.entreInput1.setText(self.delay[0])
            self.entreInput2.setText(self.delay[1])

        else :
            self.DelayFix.setChecked(True)
            self.fixInput.setText(self.delay)
        if self.keys is not None:
            for key in self.keys:
                key= self.string_to_key(key)
                try:
                    key= key.char
                    print(f'loaded {key}')
                except AttributeError:
                    # key = self.string_to_key(key)
                    print(f'loaded {key}')
                self.list.addItem(str(key))

    def string_to_key(self, key):
        """
        Convertit une chaîne de caractères en un objet Key de pynput.

        :param key_string: La chaîne représentant la touche (ex. "Key.enter").
        :return: L'objet Key correspondant (ex. Key.enter).
        """
        try:
            # Supprimer le préfixe 'Key.' de la chaîne et obtenir l'objet Key correspondant
            if key.startswith('Key.'):
                key_name = key.split('.')[1]
                return getattr(Key, key_name)
            else:
                # Si ce n'est pas une touche spéciale, retourner la chaîne elle-même (pour touches normales)
                return key
        except AttributeError:
            raise ValueError(f"Touche non reconnue: {key}")

    def Play(self):
        self.delay=None
        self.time=None
        self.keys = [self.string_to_key(self.list.item(i).text()) for i in range(self.list.count())]
        if self.keys != []:
            if self.DelayFix.isChecked() :
                if self.fixInput.text() != '':
                    self.delay = self.fixInput.text()
                    self.delay = self.delay.replace(",", ".")
                else :
                    self.delay=None

            else :
                self.delay = [self.entreInput1.text().replace(",", "."),self.entreInput2.text().replace(",", ".")]
            if self.TimeFix.isChecked():
                if self.time != '':
                    self.time = self.timeFixInput.text()
                    self.time = self.time.replace(",", ".")
                else :
                    self.time=None
            else :
                self.time = 'inf'

            if self.DelayFix.isChecked() or self.DelayAlea.isChecked() and self.TimeFix.isChecked() or self.TimeInf.isChecked():
                # print(all(x is not None and '' not in x for x in [self.delay, self.time, self.keys]))
                vide = '\'\''
                if all(x is not None and vide not in x for x in [self.delay, self.time, self.keys]):                
                    PlayFile.start_simulation(self.delay,self.time,self.keys)

    def Stop(self):
        PlayFile.stop_simulation()
        print('Stopped')