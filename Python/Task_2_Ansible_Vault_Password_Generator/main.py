import random
import pickle
import yaml
import os
from ruled_password_generator import PasswordGenerator
from cryptography.fernet import Fernet

#config for generating user and password
length_password = random.randint(24, 48)
length_user = random.randint(8, 12)
rules_for_password = {
    "min_lowercase": 1,
    "min_uppercase": 1,
    "min_digits": 1,
    "min_special": 1
}
rules_for_user = {
    "min_lowercase": 1,
    "min_uppercase": 1,
    "min_digits": 1,
}

#Generate user and password
pwg_password = PasswordGenerator(length_password, rules=rules_for_password)
password = pwg_password.generate()
pwg_user = PasswordGenerator(length_user, rules=rules_for_user)
print("Plain password: ", password)
user = pwg_user.generate()
print("Plain user: ", user)

data = {
    "user": user,
    "password": password
}
yaml_bytes = yaml.dump(data).encode()

#Generate fernet key
key = Fernet.generate_key()
f = Fernet(key)
encrypted = f.encrypt(yaml_bytes)

#Save as vault file
with open ('.vault_pass', 'w') as outfile:
    outfile.write("$ANSIBLE_VAULT;1.1;AES256\n")
    outfile.write(encrypted.decode())
    #pickle.dump(encrypted,outfile)
os.chmod('.vault_pass', 600)
with open ('key.secret', 'w') as keyfile:
    keyfile.write(key.decode())
    #pickle.dump(key.decode(), keyfile)
print("Saved encrypted file, key: ", key.decode())
