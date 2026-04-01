n=input("num: ")

if n[-1]=="0" or n[-1]=="2" or n[-1]=="4" or n[-1]=="6" or n[-1]=="8":
    print(True)

if not (n[-1]=="0" or n[-1]=="2" or n[-1]=="4" or n[-1]=="6" or n[-1]=="8"):
    print(False)