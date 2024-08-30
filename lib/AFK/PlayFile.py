import time
import threading
from pynput.keyboard import Listener, KeyCode, Controller, Key
import random

stop_event = threading.Event()

def playFunc(delay, duration, keys):
    print('play')
    stop_event.clear()
    """
    Simule des appuis de touches sur une durée spécifiée avec un délai défini.

    :param delay: Délai en secondes entre chaque pression de touche.
    :param duration: Durée totale de la simulation en secondes ou 'inf' pour une durée infinie.
    :param keys: Liste des touches à simuler (ex. ['a', 'b', 'c']).
    """
    keyboard = Controller()

    if '\'\'' not in delay:
        if isinstance(delay,list):
            print(type(delay))
            print(delay)
            delay = [float(s) for s in delay]
        else:
            delay = float(delay)
    else :
        delay =None
    if duration != 'inf':
        duration = float(duration)
        end_time = time.time() + duration
    else:
        end_time = float('inf')  # Durée infinie

    while time.time() < end_time:
        if stop_event.is_set():
            print("Simulation arrêtée.")
            return

        for key in keys:
            if stop_event.is_set():
                print("Simulation arrêtée.")
                return

            try:
                # Simuler l'appui de la touche
                keyboard.press(key)
                keyboard.release(key)
                print('key {0} pressed'.format(key))
            except AttributeError:
                print('special key {0} pressed'.format(key))
            # Attendre le délai défini avant la prochaine touche
            if isinstance(delay, list) and delay != ['','']:
                print('delay != ['','']')
                time.sleep(random.uniform(delay[0],delay[1]))
            elif delay is not None:
                time.sleep(delay)


def start_simulation(delay, duration, keys):
    """
    Démarre la simulation des frappes dans un thread séparé.

    :param delay: Délai en secondes entre chaque pression de touche.
    :param duration: Durée totale de la simulation en secondes ou 'inf' pour une durée infinie.
    :param keys: Liste des touches à simuler (ex. ['a', 'b', 'c']).
    """
    global stop_event
    stop_event.clear()  # Réinitialiser l'événement avant de commencer
    thread = threading.Thread(target=playFunc, args=(delay, duration, keys))
    thread.start()
    return thread

def stop_simulation():
    """
    Arrête la simulation en cours.
    """
    global stop_event
    stop_event.set()  # Signale au thread de s'arrêter
