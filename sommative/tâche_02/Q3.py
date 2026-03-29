# Grant Philippe-Daniel
#Ce programme demande une Le prix d'une achat et calcul le rabais dependant sur le prix.


import os
os.system('cls' if os.name == 'nt' else 'clear')


Prix=float(input("Quel etait le prix d'achat?:"))
print (Prix)

Rabais=0
if Prix < 50:
    Rabais=0
if Prix >= 50:
    Rabais=0.10
if Prix >=100:
    Rabais=0.15

RabaisTotale=Prix*Rabais
print ("Le rabais est ",(RabaisTotale))

SommeTotale=Prix-RabaisTotale
print("La somme apres rabais est", SommeTotale)

Taxe=SommeTotale*0.13
print("La taxe est", Taxe)

TotalFinal=SommeTotale+Taxe
print("Le total final est", TotalFinal)