try:

    entreeAge = input("Entrez votre âge : ")

    monAge = int(entreeAge)

except:
    raise Exception("Erreur : l'âge doit être un nombre entier.")

else:
    print("Vous avez", monAge, "ans.")