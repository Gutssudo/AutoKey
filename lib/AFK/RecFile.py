from pynput import keyboard


def RecFunc():
    # Variable pour stocker la touche appuyée
    key_pressed = None

    def on_press(key):
        nonlocal key_pressed
        try:
            # Afficher le caractère de la touche appuyée
            print(f"Touche appuyée: {key.char}")
            key_pressed = key.char
        except AttributeError:
            # Afficher le nom de la touche spéciale
            print(f"Touche spéciale appuyée: {key}")
            key_pressed = key  # Convertir la touche spéciale en chaîne de caractères
        # Arrêter l'écoute après la première touche appuyée
        return False  # Retourner False arrête le listener

    # Créer un écouteur de clavier
    with keyboard.Listener(on_press=on_press) as listener:
        print("Appuyez sur une touche...")
        listener.join()  # Attendre les événements du clavier

    # Retourner la touche appuyée après que le listener a arrêté
    return key_pressed