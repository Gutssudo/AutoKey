import csv
import re
import yaml
import os
import sys

# Fonction pour obtenir le chemin du fichier en tenant compte de PyInstaller
def resource_path(relative_path):
    """Retourne le chemin absolu en prenant en compte PyInstaller"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Charger les correspondances depuis le fichier CSV
def load_key_mappings(file, source, result):
    key_mappings = {}
    file_path = resource_path(file)
    
    with open(file_path, mode='r', newline='') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if len(row) == 2:
                key1, key2 = row
                key_mappings[key1.strip()] = key2.strip()
    return key_mappings

# Traduire les touches en utilisant les mappings
def TradPyMgp(keys, source, result):
    file = 'translate.csv'
    key_mappings = load_key_mappings(file, source, result)
    translated_keys = []
    start_key = ""

    for key in keys:
        key = key.strip()
        if source == 'pynput_key' and result == 'Code':
            translated_key = key_mappings.get(key, "Touche non trouvée")
        elif source == 'Code' and result == 'pynput_key':
            match = re.search(r"bindedkey=([A-Za-z])", key)
            if match:
                start_key = match.group(1)

            inverse_mappings = {v: k for k, v in key_mappings.items()}
            translated_key = ['', '']
            prefix_suffix = extract_prefix(key)
            if prefix_suffix:
                prefix, suffix = prefix_suffix
                translated_key[0] = inverse_mappings.get(prefix, prefix).replace('_r', '_l')
                translated_key[1] = suffix
        else:
            translated_key = "Source ou résultat non reconnu"

        translated_keys.append(translated_key)

    if start_key:
        return translated_keys, suffix, start_key
    return translated_keys, suffix

# Extraction du préfixe et du suffixe des touches
def extract_prefix(key):
    patternSpeChar = r'^(SHIFT|CTRL|ALT)(UP|DOWN)$'
    matchSpeChar = re.match(patternSpeChar, key)

    patternChar = r'^([a-z])\s+(down|up)$'
    matchChar = re.match(patternChar, key)

    patternDelay = r'^(\d+)\s(D)$'
    matchDelay = re.match(patternDelay, key)

    if matchSpeChar:
        return matchSpeChar.group(1), matchSpeChar.group(2)
    if matchChar:
        return matchChar.group(1), matchChar.group(2)
    if matchDelay:
        return matchDelay.group(1), matchDelay.group(2)

    return None

# Traduire un fichier YAML
def TradYamlPy(file):
    file_path = resource_path(file)
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)

    start_key = data.get('StartKey', None)
    actions = []

    for action in data['actions']:
        if 'delay' in action:
            actions.append(['delay', action['delay']])
        else:
            actions.append([action['key'], 'presser' if action['event'] == 'down' else 'relâcher'])

    return start_key, actions
