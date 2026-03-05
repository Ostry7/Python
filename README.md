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


### Task 4 PostgreSQL Backup Automation [v]

Create:
- Script using `pg_dump`
- Compress backup with gzip
- Upload to S3 (boto3) or local storage


### Key components:

1. `pg_backup.py`:

First of all the code trying to establish connection with `DB_HOST` and then try to create a `backup.sql` using the `pg_dump`.
If the backup is created successfully next step is being performed ---> using `gzip` it will compress database dump as `backup.sql.gz` file.

2. `aws_s3_push.py`:

Using `boto3` the script will try to upload file to the AWS S3.

3. `main.py`:

The main file where all functions is being call.


### Task 5: Docker Resource Monitor [v]

Create:
- Connect to Docker daemon using docker-py
- Collect CPU/memory/disk metrics for all containers
- Alert when usage >80% (print + JSON webhook)
- Continuous monitoring loop 

### Key components:

To connect to the docker daemon we're using:
```python
client = docker.from_env() #connect to the daemon
containers = client.containers.list(all=False) #list of containers -> docker ps
```

We're collecting CPU and memory usage for all running containers using `def collect_cpu_and_mem()` function. Then we have a `def monitor(cpu_threshold, mem_threshold, monitoring_interval):` function with `cpu_threshold`, `mem_threshold` and `monitoring_interval` parameters.  Both functions have `while True` set infinite loop to all the time generate usage stats and to monitor them. All the data are saved in `stats.json` file.