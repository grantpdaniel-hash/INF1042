while True:
    nom = input("Entrez votre nom: ")

    if len(nom) >= 8 and len(nom) <= 12:
        print("Bonjour,", nom, "!")
        break
    else:
        print("Le nom doit contenir entre 8 et 12 caractères.")