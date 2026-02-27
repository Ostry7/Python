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

### Task 3: Terraform File Validator [v]

Create:
- Directory scanner for .tf files
- Run terraform validate on each module
- Parse HCL syntax errors with hcl2json
- Generate validation-report.md with pass/fail status
- Handle missing Terraform gracefully

### Key elements:

1. Directory scanner for `.tf` files:
I'm using the `os` module to search `.tf` files:
```python
        elif entry.endswith('.tf'):
            terraform_files_list.append(full_path)
```

2. Run terraform validate on each module:
I'm using `subprocess` module to validate terraform:
```python
            result = subprocess.run(['terraform', 'validate', terraform_file],
                                  capture_output=True, text=True, timeout=10)
```

3. Parse HCL syntax errors with hcl2json:
Using the `hcl2` module we can check syntax errors:
```python
    for terraform_file in terraform_files_list:
        try:
            with open (terraform_file, 'r') as file:
                dict = hcl2.load(file)
            status = "[v] PASS"

        except Exception as e:
            status = f'[X] FAIL: {e}'
```

4. Generate validation-report.md with pass/fail status
Using  `markdown_table` I we can create a MD table:
```python
    for result in hcl_results:
        filename = os.path.basename(result['file'])
        status = result['status'][:40]
        result = "[v]" if "[v]" in status else "[X]"
        
        table_data.append({"File": filename, "Status": status, "Result": result})
    
    markdown_table_obj = markdown_table(table_data)
    markdown = markdown_table_obj.get_markdown()
```


### Task 4 PostgreSQL Backup Automation []

Create:
- Script using `psycopg2` + `pg_dump`
- Compress backup with gzip
- Upload to S3 (boto3) or local storage
- Delete backups older than retention period
- Config from .env file