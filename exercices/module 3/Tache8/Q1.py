h=int(input("heure (0-23): "))

if h==0:
    print("12am")

if h>0 and h<12:
    print(h,"am")

if h==12:
    print("12pm")

if h>12 and h<=23:
    print(h-12,"pm")