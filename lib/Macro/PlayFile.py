import time
import multiprocessing
import threading
from pynput.keyboard import Listener, KeyCode, Controller, Key
from functools import partial

# Drapeau pour contrôler la pause du listener
pause_event = multiprocessing.Event()

class PlayFile:
    def __init__(self, actions, startKey):
        self.stop_event = multiprocessing.Event()
        self.actions = actions
        self.startKey = startKey
        self.pressed_keys = []  # Liste pour suivre les touches pressées
        # Crée le processus dès l'initialisation
        self.process = multiprocessing.Process(target=self.listener_thread)
        self.process.start()  # Lancer le processus immédiatement

    def playFunc(self):
        """ Fonction appelée par le thread pour exécuter les actions """
        print('play')
        self.stop_event.clear()  # S'assurer que l'événement de stop n'est pas déclenché
        keyboard = Controller()

        for action, value in self.actions:
            if self.stop_event.is_set():
                break  # Arrêter les actions si l'événement de stop est déclenché

            try:
                if action == 'delay':
                    time.sleep(float(value) / 1000)
                    print(f'waiting : {value}')
                elif value == 'presser':
                    try:
                        keyboard.press(action)
                        self.pressed_keys.append(action)  # Ajouter la touche à la liste des touches pressées
                    except ValueError:
                        action = getattr(Key, action.split('.')[-1])
                        keyboard.press(action)
                        self.pressed_keys.append(action)
                    print(f'{action} : press')
                else:
                    try:
                        keyboard.release(action)
                        if action in self.pressed_keys:
                            self.pressed_keys.remove(action)  # Retirer la touche de la liste
                    except ValueError:
                        action = getattr(Key, action.split('.')[-1])
                        keyboard.release(action)
                        if action in self.pressed_keys:
                            self.pressed_keys.remove(action)
                    print(f'{action} : release')
            except AttributeError:
                pass

        self.release_all_keys()  # Relâcher toutes les touches à la fin
        pause_event.clear()  # Relancer le listener après l'exécution des actions

    def release_all_keys(self):
        """ Fonction pour relâcher toutes les touches qui ont été pressées """
        keyboard = Controller()
        for key in self.pressed_keys:
            try:
                keyboard.release(key)
                print(f'{key} : release (final)')
            except ValueError:
                # Gérer les touches spéciales
                key = getattr(Key, key.split('.')[-1])
                keyboard.release(key)
                print(f'{key} : release (final)')
        self.pressed_keys.clear()  # Vider la liste des touches après les avoir relâchées

    def on_press(self, key):
        """ Fonction appelée lors de l'appui sur une touche """
        if isinstance(key, KeyCode):
            key = key.char

        if str(key) == self.startKey and not pause_event.is_set():
            pause_event.set()  # Mettre en pause le listener pour éviter de déclencher d'autres actions
            # Démarrer un thread rapidement pour exécuter playFunc
            thread = threading.Thread(target=self.playFunc)
            thread.start()

    def listener_thread(self):
        """ Fonction principale du processus qui écoute les touches du clavier """
        # Utilisation de partial pour passer les paramètres à la fonction on_press
        play_with_param = partial(self.on_press)
        with Listener(on_press=play_with_param) as listener:
            while not self.stop_event.is_set():
                listener.join()  # Attendre l'appui sur une touche
                self.stop_event.wait()  # Attendre la fin de l'exécution des actions
                self.stop_event.clear()  # Réinitialiser l'événement pour le prochain déclenchement

    def killProcess(self):
        """ Fonction pour tuer le processus """
        self.stop_event.set()
        self.process.terminate()  # Terminer le processus brutalement
