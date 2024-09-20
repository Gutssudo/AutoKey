from PyQt5.QtWidgets import *
import yaml
from collections import OrderedDict

def save(parent, startKey, actions):
    """
    Fonction pour ouvrir une boîte de dialogue et enregistrer un fichier YAML avec la liste d'actions.
    """
    # Formater les actions brutes pour les sauvegarder dans un fichier YAML
    data = formatSave(startKey, actions)

    # Ouvrir une boîte de dialogue pour choisir où enregistrer le fichier
    options = QFileDialog.Options()
    file_name, _ = QFileDialog.getSaveFileName(parent, "Enregistrer le fichier YAML", "",
                                               "Fichiers YAML (*.yaml);;Tous les fichiers (*)", options=options)

    if file_name:  # Vérifie si un nom de fichier a été sélectionné
        # Écrire le dictionnaire dans un fichier YAML
        with open(file_name, 'w') as file:
             yaml.dump(data, file, default_flow_style=False, allow_unicode=True, sort_keys=False)  # Ajout de sort_keys=False
        print("Fichier YAML créé avec succès à l'emplacement:", file_name)


def formatSave(startKey, raw_actions):
    """
    Formater les données pour le fichier YAML avec le StartKey et la liste des actions brutes.
    Chaque action peut être soit une touche avec une action (presser ou relâcher), soit un délai.
    """
    # Créer la structure des données à sauvegarder avec un dictionnaire simple
    data = {
        "StartKey": startKey,  # La clé de démarrage
        "actions": []          # Liste d'actions formatées
    }

    # Traiter chaque action brute
    for action in raw_actions:
        if action[0] == 'delay':
            # Si l'action est un délai, on l'ajoute avec la clé 'delay'
            delay_time = int(action[1])  # Convertir le délai en millisecondes
            data["actions"].append({"delay": delay_time})
        else:
            # Si l'action est une touche à presser ou relâcher
            key = action[0]
            event = 'down' if action[1] == 'presser' else 'up'  # 'presser' -> 'down', 'relâcher' -> 'up'
            data["actions"].append({
                "key": key,
                "event": event
            })

    return data