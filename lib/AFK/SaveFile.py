from PyQt5.QtWidgets import *
import yaml

def save(parent, keys, delay,time):
    # Ouvrir la boîte de dialogue pour choisir le fichier
    data = formatSave(keys, delay,time)
    # Ouvrir une boîte de dialogue pour choisir où enregistrer le fichier
    options = QFileDialog.Options()
    file_name, _ = QFileDialog.getSaveFileName(parent, "Enregistrer le fichier YAML", "",
                                               "Fichiers YAML (*.yaml);;Tous les fichiers (*)", options=options)

    if file_name:  # Vérifie si un nom de fichier a été sélectionné
        # Écrire le dictionnaire dans un fichier YAML
        with open(file_name, 'w') as file:
            yaml.dump(data, file, default_flow_style=False, allow_unicode=True)
        print("Fichier YAML créé avec succès à l'emplacement:", file_name)


def formatSave(keys, delay,time):
    # Créer un dictionnaire avec les variables et la liste d'objets
    data = {
        "delay": delay,
        "time": time,
        "keys": keys
    }
    return data
