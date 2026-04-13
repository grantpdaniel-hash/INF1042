matchs = (
    ("Tigres", "Lynx", 25, 18),
    ("Aigles", "Panthères", 22, 25),
    ("Tigres", "Panthères", 25, 23),
    ("Lynx", "Aigles", 19, 25),
    ("Tigres", "Aigles", 21, 25),
    ("Lynx", "Panthères", 25, 20)
)

victoires = {}
defaites = {}
points = {}

for equipe1, equipe2, score1, score2 in matchs:

    if equipe1 not in victoires:
        victoires[equipe1] = 0
        defaites[equipe1] = 0
        points[equipe1] = 0

    if equipe2 not in victoires:
        victoires[equipe2] = 0
        defaites[equipe2] = 0
        points[equipe2] = 0

    points[equipe1] += score1
    points[equipe2] += score2

    if score1 > score2:
        print("Les", equipe1, "ont battu les", equipe2, "par", score1, "à", score2)
        victoires[equipe1] += 1
        defaites[equipe2] += 1
    else:
        print("Les", equipe2, "ont battu les", equipe1, "par", score2, "à", score1)
        victoires[equipe2] += 1
        defaites[equipe1] += 1

print()

print("Nombre de victoires :")
for equipe in victoires:
    print(equipe, ":", victoires[equipe])

print()

max_victoires = max(victoires, key=victoires.get)
print("Équipe avec le plus de victoires :", max_victoires)

print()

print("Total de points :")
for equipe in points:
    print(equipe, ":", points[equipe])

print()

max_points = max(points, key=points.get)
print("Équipe avec le plus de points :", max_points)

print()

for equipe in victoires:
    if victoires[equipe] > defaites[equipe]:
        print(equipe, "a plus de victoires que de défaites")
    elif victoires[equipe] == defaites[equipe]:
        print(equipe, "a autant de victoires que de défaites")
    else:
        print(equipe, "a plus de défaites que de victoires")