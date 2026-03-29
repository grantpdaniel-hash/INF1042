# Nom : Grant Philippe-Daniel
# Ce programme affiche le nombre moyen de jours dans un mois pour une année normale et une année bissextile.
# Clear the terminal
import os
os.system('cls' if os.name == 'nt' else 'clear')

jours_normale=365
moyenne_normale=jours_normale/12
print("Pour une année normale la moyenne de jours dans une mois est:")
print(moyenne_normale)

jours_bissextile = 366
moyenne_bissextile = jours_bissextile / 12
print("Pour une année bissextile la moyenne de jours dans une mois est:")
print(moyenne_bissextile)