import random

A = set(random.randint(1, 20) for _ in range(10))
B = set(random.randint(1, 20) for _ in range(10))

print(A)
print(B)
print(A|B)
print(A&B)
print(A-B)