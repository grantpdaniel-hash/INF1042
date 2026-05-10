achats = [
    ("Liam", "Galaxy Battle", "PC", 59.99),
    ("Emma", "Speed Zone", "PlayStation", 49.99),
    ("Liam", "Pixel Quest", "Switch", 39.99),
    ("Noah", "Galaxy Battle", "PC", 59.99),
    ("Emma", "Sky Builder", "PC", 29.99),
    ("Olivia", "Speed Zone", "Xbox", 54.99),
    ("Liam", "Sky Builder", "PC", 29.99),
    ("Noah", "Pixel Quest", "Switch", 39.99)
]
 
# 1. Afficher tous les achats
print("Tous les achats:")
for achat in achats:
    nom_client, titre_jeu, plateforme, prix = achat
    print(" -", nom_client, "a acheté", titre_jeu, "sur", plateforme, "pour", prix, "$")
 
# 2. Ensemble de tous les titres uniques
titres_uniques = set()
for achat in achats:
    titres_uniques.add(achat[1])
print("Jeux uniques:", titres_uniques)
 
# 3. Ensemble de toutes les plateformes uniques
plateformes_uniques = set()
for achat in achats:
    plateformes_uniques.add(achat[2])
print("Plateformes uniques:", plateformes_uniques)
 
# 4. Montant total dépensé par tous les clients
total_depense = 0
for achat in achats:
    total_depense += achat[3]
print("Total dépensé:", total_depense, "$")
 
# 5. Dictionnaire : argent dépensé par client
depenses_clients = {}
for achat in achats:
    nom_client = achat[0]
    prix = achat[3]
    if nom_client in depenses_clients:
        depenses_clients[nom_client] += prix
    else:
        depenses_clients[nom_client] = prix
print("Dépenses par client:", depenses_clients)
 
# 6. Client qui a dépensé le plus
client_max = ""
montant_max = 0
for client, montant in depenses_clients.items():
    if montant > montant_max:
        montant_max = montant
        client_max = client
print("Client qui a dépensé le plus:", client_max, "-", montant_max, "$")
 
# 7. Dictionnaire : nombre de fois que chaque jeu a été acheté
achats_par_jeu = {}
for achat in achats:
    jeu = achat[1]
    if jeu in achats_par_jeu:
        achats_par_jeu[jeu] += 1
    else:
        achats_par_jeu[jeu] = 1
print("Achats par jeu:", achats_par_jeu)
 
# 8. Achats faits sur PC seulement
print("Achats sur PC:")
for achat in achats:
    if achat[2] == "PC":
        nom_client, titre_jeu, plateforme, prix = achat
        print(" -", nom_client, "a acheté", titre_jeu, "pour", prix, "$")
 
# 9. Résumé final
jeu_plus_achete = ""
max_achats = 0
for jeu, nb in achats_par_jeu.items():
    if nb > max_achats:
        max_achats = nb
        jeu_plus_achete = jeu
 
print("Nombre total d'achats:", len(achats))
print("Jeux uniques:", titres_uniques)
print("Plateformes uniques:", plateformes_uniques)
print("Client qui a dépensé le plus:", client_max, "-", montant_max, "$")
print("Jeu le plus acheté:", jeu_plus_achete, "-", max_achats, "fois")
 