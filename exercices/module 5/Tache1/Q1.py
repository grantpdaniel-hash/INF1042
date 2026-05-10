import math


class Forme:

    def __init__(self, longueur):
        self.longueur = longueur

    def aire(self):
        pass

    def perimetre(self):
        pass


class Cercle(Forme):

    def aire(self):

        rayon = self.longueur

        return math.pi * rayon * rayon

    def perimetre(self):

        rayon = self.longueur

        return 2 * math.pi * rayon


class Triangle(Forme):

    def aire(self):

        cote = self.longueur

        return (math.sqrt(3) / 4) * (cote * cote)

    def perimetre(self):

        cote = self.longueur

        return cote * 3


class Rectangle(Forme):

    def aire(self):

        cote = self.longueur

        return cote * cote

    def perimetre(self):

        cote = self.longueur

        return cote * 4


class Pentagon(Forme):

    def aire(self):

        cote = self.longueur

        return (5 * (cote * cote)) / (4 * math.tan(math.pi / 5))

    def perimetre(self):

        cote = self.longueur

        return cote * 5


class Hexagon(Forme):

    def aire(self):

        cote = self.longueur

        return ((3 * math.sqrt(3)) / 2) * (cote * cote)

    def perimetre(self):

        cote = self.longueur

        return cote * 6


class Heptagon(Forme):

    def aire(self):

        cote = self.longueur

        return (7 * (cote * cote)) / (4 * math.tan(math.pi / 7))

    def perimetre(self):

        cote = self.longueur

        return cote * 7


class Octagon(Forme):

    def aire(self):

        cote = self.longueur

        return 2 * (1 + math.sqrt(2)) * (cote * cote)

    def perimetre(self):

        cote = self.longueur

        return cote * 8


maShape1 = Cercle(5)
print("Cercle")
print("Aire =", maShape1.aire())
print("Perimetre =", maShape1.perimetre())

print()

maShape2 = Triangle(5)
print("Triangle")
print("Aire =", maShape2.aire())
print("Perimetre =", maShape2.perimetre())

print()

maShape3 = Rectangle(5)
print("Rectangle")
print("Aire =", maShape3.aire())
print("Perimetre =", maShape3.perimetre())

print()

maShape4 = Pentagon(5)
print("Pentagon")
print("Aire =", maShape4.aire())
print("Perimetre =", maShape4.perimetre())

print()

maShape5 = Hexagon(5)
print("Hexagon")
print("Aire =", maShape5.aire())
print("Perimetre =", maShape5.perimetre())

print()

maShape6 = Heptagon(5)
print("Heptagon")
print("Aire =", maShape6.aire())
print("Perimetre =", maShape6.perimetre())

print()

maShape7 = Octagon(5)
print("Octagon")
print("Aire =", maShape7.aire())
print("Perimetre =", maShape7.perimetre())