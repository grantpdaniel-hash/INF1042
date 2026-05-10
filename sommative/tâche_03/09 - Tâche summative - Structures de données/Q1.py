notes = [78, 85, 92, 67, 85, 74]
 
# 1. Affiche la liste complète
print("Liste complète:", notes)
 
# 2. Première et dernière note
print("Première note:", notes[0])
print("Dernière note:", notes[-1])
 
# 3. Ajouter la note 88
notes.append(88)
 
# 4. Supprimer la première occurrence de 85
notes.remove(85)
 
# 5. Afficher la liste mise à jour
print("Liste mise à jour:", notes)
 
# 6. Calculs
total = sum(notes)
moyenne = total / len(notes)
plus_haute = max(notes)
plus_basse = min(notes)
 
print("Total des notes:", total)
print("Moyenne:", moyenne)
print("Note la plus élevée:", plus_haute)
print("Note la plus basse:", plus_basse)