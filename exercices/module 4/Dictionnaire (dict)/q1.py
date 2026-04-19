eleve = { "nom":"Robert","age":16,"programme":"Tech"}
notes = {"math": 54, "Français": 66, "science": 100}

print(notes["science"])

notes["histoire"] = 88
notes["math"] = 82

for matiere in notes:
    print("Matière:", matiere, "| Note:", notes[matiere])