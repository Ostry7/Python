### Task 1: Apache/Nginx Log Parser [v]

Create:
- Python script that parses Apache/Nginx access logs
- Extract IP addresses from failed requests (4xx/5xx status codes)
- Count top 10 IPs with most errors
- Export results to errors.json and errors.csv

### Key elements:

There are two key element in code:
```python
ip_reg = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
```
---> to match only max 3 digits from current line using regex (matching IP addresses)

and:
```python
status_req_reg = r'"(?:GET|POST) .* (4\d{2}|5\d{2})'
```
---> to match GET or POST with error code (4xx/5xx status codes)

### Task 2: Ansible Vault Password Generator [v]

Create:
- Secure password generator (24+ chars, letters/numbers/symbols)
- Encrypt/decrypt test secret using cryptography.fernet
- Save encrypted vault password to .vault_pass (permissions 600)

1. For secure password generator I use `from ruled_password_generator import PasswordGenerator` with random user and password length. Also added some rules for creating user and password (`min_lowercase`, `min_special` etc.).

2. For encrypting I user `from cryptography.fernet import Fernet`, also exporting key as file.

3. Saving ansible vault file we need to specify a header `$ANSIBLE_VAULT;1.1;AES256\n`.