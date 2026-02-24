import random
from ruled_password_generator import PasswordGenerator

length = random.randint(24, 48)

rules = {
    "min_lowercase": 1,
    "min_uppercase": 1,
    "min_digits": 1,
    "min_special": 1
}

pwg = PasswordGenerator(length, rules=rules)
password = pwg.generate()

print(password)