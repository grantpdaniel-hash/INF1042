run=True

while run:

    print("1 entrer notes")
    print("2 moyenne")
    print("3 reussite")
    print("4 echec")
    print("5 quitter")

    ch=int(input("choix: "))

    if ch==1:
        n=int(input("combien: "))
        notes=[]
        i=0

        while i<n:
            notes.append(int(input("note: ")))
            i=i+1

    if ch==2:
        s=0
        i=0

        while i<len(notes):
            s=s+notes[i]
            i=i+1

        print(s/len(notes))

    if ch==3:
        c=0
        i=0

        while i<len(notes):
            if notes[i]>=50:
                c=c+1
            i=i+1

        print(c)

    if ch==4:
        c=0
        i=0

        while i<len(notes):
            if notes[i]<50:
                c=c+1
            i=i+1

        print(c)

    if ch==5:
        run=False