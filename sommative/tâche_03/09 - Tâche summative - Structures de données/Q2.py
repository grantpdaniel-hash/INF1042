# 1. Créer un tuple
produit = ("Clavier", 49.99, 12)
 
# 2. Afficher chaque valeur séparément
print("Nom:", produit[0])
print("Prix:", float(produit[1]))
print("Quantité:", produit[2])
 
# 3. Déballage du tuple
nom_produit, prix, quantite = produit
 
# 4. Phrase formatée
print("Le produit", nom_produit, "coûte", prix, "$ et il y en a", quantite, "en stock.")
 
# 5. Deuxième produit et comparaison de prix
produit2 = ("Souris", 29.99, 20)
 
if produit[1] > produit2[1]:
    print("Le produit le plus cher est:", produit[0])
else:
    print("Le produit le plus cher est:", produit2[0])