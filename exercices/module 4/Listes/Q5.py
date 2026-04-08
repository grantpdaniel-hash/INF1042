grille = [[1,2,3],[4,5,6],[7,8,9]]

sommes = []

for ligne in grille:
    total = sum(ligne)
    sommes.append(total)

print(sommes)