def sq(n):
    return pow(n,2)

# prend un nombre, arrondit
def rd(n):
    return round(n)

# prend texte et retourne longueur
def ln(t):
    return len(t)

n=float(input("num: "))
t=input("mot: ")

print(sq(n))
print(rd(n))
print(ln(t))