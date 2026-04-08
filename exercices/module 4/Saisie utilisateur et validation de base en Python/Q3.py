while True:
    try:
        a = float(input("Entrez une valeur float: "))
        b = float(input("Entrez une autre valeur float: "))
        break
    except:
        print("Veuillez entrer des nombres valides.")

print(a * b)
print(a - b)