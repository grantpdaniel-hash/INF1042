notes = [12, 15, 9, 18, 15, 12]

moyenne = sum(notes) / len(notes)
print(moyenne)

frequent = notes[0]
max_count = 0

for n in notes:
    count = 0
    for x in notes:
        if x == n:
            count += 1
    if count > max_count:
        max_count = count
        frequent = n

print(frequent)