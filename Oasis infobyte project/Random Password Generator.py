import random
password = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890abcdefghijklmnopqrstuvwxyz"
length_possword = int(input("Enter your password length: "))
a = "" .join(random.sample(password, length_possword))

print(f"your password is{a}")