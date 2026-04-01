import os
import random
import time

os.system('cls' if os.name == 'nt' else 'clear')

numques=int(input("combien de questions: "))

good=0
bad=0
tt=0
loop=0

while loop<numques:

    if loop<numques/3:
        n1=random.randint(1,9)
        n2=random.randint(1,9)
        op="+"

    if loop<2*numques/3:
        n1=random.randint(1,20)
        n2=random.randint(1,20)
        op=random.choice(["-","*"])

    else:
        n1=random.randint(5,50)
        n2=random.randint(1,20)
        op=random.choice(["+","-","*","/"])
        if op=="/":
            n1=n1*n2

    q=str(n1)+" "+op+" "+str(n2)+" ="

    st=time.time()
    ans=float(input(q))
    et=time.time()

    tt+=et-st

    if op=="+":
        real=n1+n2
    if op=="-":
        real=n1-n2
    if op=="*":
        real=n1*n2
    else:
        real=n1/n2

    if ans==real:
        print("bonne reponse")
        good+=1
    else:
        print("mauvaise reponse")
        bad+=1

    loop+=1

print("bonnes:",good)
print("mauvaises:",bad)
print("temps total:",round(tt,2),"sec")