import random

Fichier=open("Valeurs.txt", "w")

Loop=0
while Loop < 1000:
    Nombre=random.randint(0, 100000)
    Fichier.write(str(Nombre) + "\n")
    Loop+=1

Fichier.close()