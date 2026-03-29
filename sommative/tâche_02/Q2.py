# Grant Philippe-Daniel
# Ce programme demande une température en Celsius et la converti en Fahrenheit et en Kelvin.

import os
os.system('cls' if os.name == 'nt' else 'clear')

Celsuis=float(input("Donne moi une temperature de Celsius, "))
print("Temperature en Celsuis:" ,Celsuis)

Fahrenheit=Celsuis*9/5+32
print("Degre converti en Fahrenheit:" ,Fahrenheit)

Kelvin=Celsuis+273.15
print("Degre converti en Kelvin:" ,Kelvin)