liste_a = ["Batterie", "Basse", "Piano", "Basse", "Guitare", "Batterie"]
liste_b = ["Piano", "Voix", "Guitare", "Synthé", "Piano"]
 
# 1. Convertir en ensembles
ensemble_a = set(liste_a)
ensemble_b = set(liste_b)
 
# 2. Chansons uniques de chaque liste
print("Chansons uniques de liste A:", ensemble_a)
print("Chansons uniques de liste B:", ensemble_b)
 
# 3. Chansons dans les deux listes (intersection)
print("Dans les deux listes:", ensemble_a & ensemble_b)
 
# 4. Chansons dans une seule liste (différence symétrique)
print("Dans une seule liste:", ensemble_a ^ ensemble_b)
 
# 5. Toutes les chansons uniques combinées (union)
print("Toutes les chansons uniques:", ensemble_a | ensemble_b)