# Grant Philippe-Daniel
# Ce programme genere des nombres aleatoires entre 1 et 4 et compte combien de fois chaque nombre apparait.

import random
import os

os.system('cls' if os.name == 'nt' else 'clear')

NumSim=int(input("Combien de valeurs veut tu simuler?: "))
NumSimCom=0
Num1=0
Num2=0
Num3=0
Num4=0

while NumSimCom<NumSim:
    valeur=random.randint(1, 4)

    if valeur==1:
        Num1=Num1+1

    if valeur==2:
        Num2=Num2+1

    if valeur== 3:
        Num3=Num3+1

    if valeur==4:
        Num4=Num4+1

    NumSimCom=NumSimCom+1

Pc1 = Num1/NumSim*100
Pc2 = Num2/NumSim*100
Pc3 = Num3/NumSim*100
Pc4 = Num4/NumSim*100

print("Le Valeur 1 se represent",Num1,"fois, donc le pourcentage est",Pc1,"%")
print("Le Valeur 2 se represent",Num2,"fois, donc le pourcentage est",Pc2,"%")
print("Le Valeur 3 se represent",Num3,"fois, donc le pourcentage est",Pc3,"%")
print("Le Valeur 4 se represent",Num4,"fois, donc le pourcentage est",Pc4,"%")