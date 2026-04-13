import random

eleves = {
    "Maksym", "Léo", "Hayden", "Angel",
    "Ibrahim", "Josh", "Grant", "Maxime", "David"
}

while len(eleves) > 0:

    nom = random.choice(list(eleves))

    print(nom)

    eleves.remove(nom)

print("Tous les noms ont été choisis")