cp=input("code: ")

ok=True

if len(cp)!=7:
    ok=False

if cp[3]!=" ":
    ok=False

if not cp[0].isalpha():
    ok=False

if not cp[1].isdigit():
    ok=False

if not cp[2].isalpha():
    ok=False

if not cp[4].isdigit():
    ok=False

if not cp[5].isalpha():
    ok=False

if not cp[6].isdigit():
    ok=False

print(ok)