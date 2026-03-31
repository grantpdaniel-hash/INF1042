# Grant Philippe-Daniel
#Ce programme calcule le coût du stationnement selon le nombre d’heures elle ajoute des frais supplémentaires si nécessaire et applique un rabais si la voiture est électrique.

import os

os.system('cls' if os.name == 'nt' else 'clear')

Heures=int(input("Nombre d'heures stationnées: "))
Electrique=input("La voiture est-elle électrique (oui/non): ")

Cout=4

if Heures>1:
    Cout=Cout+(Heures-1)*3

if Heures>5:
    Cout=Cout+10

if Electrique=="oui":
    Cout=Cout*0.8

print("Le coût total du stationnement est:",Cout,"$")