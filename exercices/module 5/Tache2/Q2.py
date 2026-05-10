try:

    entree1 = input("Note 1: ")
    entree2 = input("Note 2: ")

    noteA = float(entree1)
    noteB = float(entree2)

    if noteA < 0 or noteA > 100:
        raise Exception("Erreur:note 1 invalide.")

    if noteB < 0 or noteB > 100:
        raise Exception("Erreur:note 2 invalide.")

except ValueError:
    print("Erreur: les notes doivent être numériques.")

except Exception as erreurTexte:
    print(erreurTexte)

else:

    resultat = (noteA + noteB) / 2

    print("Moyenne finale :", resultat)

finally:
    print("Fin du programme.")