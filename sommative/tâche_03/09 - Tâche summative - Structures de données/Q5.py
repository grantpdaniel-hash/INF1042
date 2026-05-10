# Liste de 4 élèves
eleves = [
    {"nom": "Ava", "niveau": 12, "activites": ["programmation", "robotique", "mathématiques"]},
    {"nom": "Liam", "niveau": 11, "activites": ["robotique", "arts"]},
    {"nom": "Mia", "niveau": 12, "activites": ["programmation", "musique", "robotique", "théâtre"]},
    {"nom": "Noah", "niveau": 10, "activites": ["mathématiques", "échecs"]}
]
 
# 1. Afficher le nom de chaque élève
print("Noms des élèves:")
for eleve in eleves:
    print(" -", eleve["nom"])
 
# 2. Élèves de 12e année
print("Élèves de 12e année:")
for eleve in eleves:
    if eleve["niveau"] == 12:
        print(" -", eleve["nom"])
 
# 3. Toutes les activités uniques
activites_uniques = set()
for eleve in eleves:
    for activite in eleve["activites"]:
        activites_uniques.add(activite)
print("Activités uniques:", activites_uniques)
 
# 4. Élève avec le plus grand nombre d'activités
eleve_max = eleves[0]
for eleve in eleves:
    if len(eleve["activites"]) > len(eleve_max["activites"]):
        eleve_max = eleve
print("Élève avec le plus d'activités:", eleve_max["nom"])
 
# 5. Combien d'élèves participent à la robotique
compteur_robotique = 0
for eleve in eleves:
    if "robotique" in eleve["activites"]:
        compteur_robotique += 1
print("Élèves en robotique:", compteur_robotique)