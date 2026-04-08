phrase = "Le petit ordinateur triste oublia ses rêves et pleura dans le silence."

mots = phrase.split()

inverse = mots[::-1]

for mot in inverse:
    print(mot, end=" ")