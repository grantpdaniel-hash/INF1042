n=int(input("num: "))

if n%3==0 and n%5==0:
    print("divisible par 3 et 5")

if n%3==0 and not n%5==0:
    print("divisible par 3")

if n%5==0 and not n%3==0:
    print("divisible par 5")

if not n%3==0 and not n%5==0:
    print("aucune")