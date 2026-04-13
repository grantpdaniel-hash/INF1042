fichier=open("Valeurs.txt", "r")
Bas=open("Bas.txt", "w")
Haut=open("Haut.txt", "w")

for loop in fichier:
    num=int(loop.strip())
    if num <= 49999:
        Bas.write(str(num) + "\n")
    if num >= 50000:
        Haut.write(str(num) + "\n")

fichier.close()
Bas.close()
Haut.close()