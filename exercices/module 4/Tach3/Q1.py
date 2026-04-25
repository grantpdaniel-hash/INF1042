import random

liste = [random.randint(1, 20) for _ in range(100)]
set_unique = set(liste)
liste_triee = sorted(list(set_unique))

print(liste)
print(liste_triee)