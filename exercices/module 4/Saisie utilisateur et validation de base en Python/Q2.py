nom = input("Entrez votre nom: ")

while True:
    age = input("Entrez votre âge: ")

    if age.isdigit():
        age = int(age)
        break
    else:
        print("Veuillez entrer un âge valide.")

print(nom + ", dans 5 ans, tu auras", age + 5, "ans.")