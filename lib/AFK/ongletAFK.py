# onglet_afk.py
import os
import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget,
    QCheckBox, QButtonGroup, QLineEdit, QFileDialog
)
from PyQt5.QtGui import QIcon, QDoubleValidator
from . import RecFile, LoadFile, SaveFile, PlayFile
from pynput.keyboard import Key, KeyCode

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class OngletAFK(QWidget):
    def __init__(self):
        super().__init__()
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

        self.list = QListWidget()
        self.mainLayout.addWidget(self.list)

        self.topLayout = QHBoxLayout()

        self.timeLayout = QVBoxLayout()
        self.TimeLabel = QLabel("Time:")
        self.timeLayout.addWidget(self.TimeLabel)

        self.timeFixLayout = QHBoxLayout()
        self.TimeFix = QCheckBox("Fix")
        self.timeFixInput = QLineEdit()
        self.timeFixInput.setPlaceholderText("time (s)")
        self.timeFixInput.setValidator(QDoubleValidator(0.99, 99.99, 2))

        self.timeFixLayout.addWidget(self.TimeFix)
        self.timeFixLayout.addWidget(self.timeFixInput)

        self.timeInfLayout = QHBoxLayout()
        self.TimeInf = QCheckBox("Inf")
        self.timeInfLayout.addWidget(self.TimeInf)

        self.timeLayout.addLayout(self.timeFixLayout)
        self.timeLayout.addLayout(self.timeInfLayout)

        self.buttonGroupTime = QButtonGroup()
        self.buttonGroupTime.addButton(self.TimeInf)
        self.buttonGroupTime.addButton(self.TimeFix)
        self.buttonGroupTime.setExclusive(True)

        self.topLayout.addLayout(self.timeLayout)

        self.DelayLayout = QVBoxLayout()
        self.DelayLabel = QLabel("Delay :")
        self.DelayLayout.addWidget(self.DelayLabel)

        self.fixLayout = QHBoxLayout()
        self.DelayFix = QCheckBox("Fix")
        self.fixInput = QLineEdit()
        self.fixInput.setValidator(QDoubleValidator(0.99, 99.99, 2))
        self.fixInput.setPlaceholderText("delay (s)")

        self.fixLayout.addWidget(self.DelayFix)
        self.fixLayout.addWidget(self.fixInput)

        self.DelayLayout.addLayout(self.fixLayout)

        self.entreLayout = QHBoxLayout()
        self.DelayAlea = QCheckBox("Entre")
        self.entreInput1 = QLineEdit()
        self.entreInput1.setPlaceholderText("min (s)")
        self.entreInput2 = QLineEdit()
        self.entreInput2.setPlaceholderText("max (s)")
        self.entreInput1.setValidator(QDoubleValidator(0.99, 99.99, 2))
        self.entreInput2.setValidator(QDoubleValidator(0.99, 99.99, 2))

        self.entreLayout.addWidget(self.DelayAlea)
        self.entreLayout.addWidget(self.entreInput1)
        self.entreLayout.addWidget(QLabel("et"))
        self.entreLayout.addWidget(self.entreInput2)

        self.DelayLayout.addLayout(self.entreLayout)

        self.buttonGroupDelay = QButtonGroup()
        self.buttonGroupDelay.addButton(self.DelayFix)
        self.buttonGroupDelay.addButton(self.DelayAlea)
        self.buttonGroupDelay.setExclusive(True)

        self.topLayout.addLayout(self.DelayLayout)
        self.mainLayout.addLayout(self.topLayout)

        self.mainLayout.addStretch()

        self.SaveButton = QPushButton("Save")
        self.mainLayout.addWidget(self.SaveButton)
        self.SaveButton.clicked.connect(self.save_yaml)
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

    def open_file_dialog(self):
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
        self.keys = [self.list.item(i).text() for i in range(self.list.count())]
        if self.DelayFix.isChecked():
            self.delay = self.fixInput.text()
        else:
            self.delay = [self.entreInput1.text(), self.entreInput2.text()]
        if self.TimeFix.isChecked():
            self.time = self.timeFixInput.text()
        else:
            self.time = 'inf'
        SaveFile.save(self, self.keys, self.delay, self.time)

    def loadFile(self):
        self.Reset()
        file = self.open_file_dialog()
        self.time, self.delay, self.keys = LoadFile.LoadFunc(file)
        if self.time != 'inf':
            self.TimeFix.setChecked(True)
            self.timeFixInput.setText(self.time)
        else:
            self.TimeInf.setChecked(True)
        if isinstance(self.delay, list):
            self.DelayAlea.setChecked(True)
            self.entreInput1.setText(self.delay[0])
            self.entreInput2.setText(self.delay[1])
        else:
            self.DelayFix.setChecked(True)
            self.fixInput.setText(self.delay)
        if self.keys is not None:
            for key in self.keys:
                key = self.string_to_key(key)
                try:
                    key = key.char
                    print(f'loaded {key}')
                except AttributeError:
                    print(f'loaded {key}')
                self.list.addItem(str(key))

    def string_to_key(self, key):
        try:
            if key.startswith('Key.'):
                key_name = key.split('.')[1]
                return getattr(Key, key_name)
            else:
                return key
        except AttributeError:
            raise ValueError(f"Touche non reconnue: {key}")

    def Play(self):
        self.delay = None
        self.time = None
        self.keys = [self.string_to_key(self.list.item(i).text()) for i in range(self.list.count())]
        if self.keys != []:
            if self.DelayFix.isChecked():
                if self.fixInput.text() != '':
                    self.delay = self.fixInput.text().replace(",", ".")
                else:
                    self.delay = None
            else:
                self.delay = [self.entreInput1.text().replace(",", "."), self.entreInput2.text().replace(",", ".")]
            if self.TimeFix.isChecked():
                if self.time != '':
                    self.time = self.timeFixInput.text().replace(",", ".")
                else:
                    self.time = None
            else:
                self.time = 'inf'

            if (self.DelayFix.isChecked() or self.DelayAlea.isChecked()) and (self.TimeFix.isChecked() or self.TimeInf.isChecked()):
                vide = '\'\''
                if all(x is not None and vide not in x for x in [self.delay, self.time, self.keys]):
                    PlayFile.start_simulation(self.delay, self.time, self.keys)

    def Stop(self):
        PlayFile.stop_simulation()
        print('Stopped')
