# from PyQt5.QtWidgets import *
import yaml
def LoadFunc(file):
    try :
        with open(file, 'r') as file:
            data = yaml.safe_load(file)
        delay = data.get('delay')
        time = data.get('time')

        # Accéder à la liste d'objets
        keys = data.get('keys', [])

    except:
        time = None
        delay = None
        keys = None

    return time, delay, keys

