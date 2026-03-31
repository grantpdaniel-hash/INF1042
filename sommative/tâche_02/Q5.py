# Grant Philippe-Daniel 
#Ce programme permet à l'utilisateur de jouer à pierre, papier, ciseaux contre l'ordinateur, en générant un choix aléatoire, en comparant les résultats et en gardant un compte des victoires et défaites.

import random
import os

gagne=0
perdu=0
continuer="oui"

while continuer=="oui":
    os.system('cls' if os.name == 'nt' else 'clear')

    Choix=input("Choisissez une option, pierre, papier, ou ciseaux:")
    Ordinateur=random.randint(1, 3)
    
    if Ordinateur==1:
        Ordinateur="pierre"
    if Ordinateur==2:
        Ordinateur="papier"
    if Ordinateur==3:
        Ordinateur="ciseaux"

    if Choix.isalpha():
        print("Vous avez choisi", Choix)
        print("Ordinateur a choisi", Ordinateur)

    if Choix==Ordinateur:
        print("Wow! Vous avez choisi la meme reponse,", Ordinateur)

    if (Choix=="pierre" and Ordinateur=="ciseaux") or \
        (Choix=="papier" and Ordinateur=="pierre") or \
        (Choix=="ciseaux" and Ordinateur=="papier"):
        print("Vous avez gagne! Bravo")
        gagne=gagne+1

    else:
        print("Vous avez perdu ;)")
        perdu=perdu+1

    continuer=input("Voulez-vous continuer,oui ou non?")

print("Résultats finaux:")
print("Tu as Gagné:", gagne, "fois")
print("Tu as Perdu:", perdu, "fois")