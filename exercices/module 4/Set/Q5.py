eleves_A = {"Mia", "Noah", "Liam", "Zoe"}

eleves_B = {"Zoe", "Emma", "Liam", "Olivier"}

seulement_A = eleves_A.difference(eleves_B)

difference_symetrique = eleves_A.symmetric_difference(eleves_B)

print("Dans A seulement :", seulement_A)

print("Différence symétrique :", difference_symetrique)