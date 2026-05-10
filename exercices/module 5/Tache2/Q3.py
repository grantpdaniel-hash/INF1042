argentCompte = 250.00

try:

    retraitTexte = input("Montant à retirer : ")

    retraitTexte = retraitTexte.replace("$", "")

    retraitArgent = float(retraitTexte)

    if retraitArgent <= 0:
        raise Exception("Erreur : montant invalide.")

    if retraitArgent > argentCompte:
        raise Exception("Erreur : fonds insuffisants.")

except ValueError:
    print("Erreur : entrée invalide.")

except Exception as probleme:
    print(probleme)

else:

    argentCompte = argentCompte - retraitArgent

    print("Retrait accepté.")
    print("Nouveau solde :", argentCompte, "$")

finally:
    print("Fin de la transaction.")