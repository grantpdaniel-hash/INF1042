fichier=open("valeurs.txt", "r")

maxval=-1
minval=100001
total=0
count=0

for loop in fichier:
    num=int(loop.strip())
    if num>maxval:
        maxval=num
    if num<minval:
        minval=num
    total+=num
    count+=1

fichier.close()

print("max:", maxval)
print("min:", minval)
print("moy:", total/count)