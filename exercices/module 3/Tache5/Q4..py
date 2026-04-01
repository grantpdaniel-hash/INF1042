pw=0
def check(pw):
    hasnum=False
    haslet=False

    i=0
    while i<len(pw):
        if pw[i].isdigit():
            hasnum=True
        if pw[i].isalpha():
            haslet=True
        i=i+1

    if hasnum and haslet and len(pw)>=8:
        return True

    if not (hasnum and haslet and len(pw)>=8):
        return False


pw=input("pw: ")
print(check(pw))