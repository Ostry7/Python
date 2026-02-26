import os
import hcl2
import subprocess

directory_path = './terraform/'
terraform_files_list = []

def list_terraform_files (path = '.'):
    for entry in os.listdir(path):
        full_path = os.path.join(path,entry)
        if os.path.isdir(full_path):
            list_terraform_files(full_path)
        elif entry.endswith('.tf'):
            #print (full_path)
            terraform_files_list.append(full_path)

def terraform_validate():  
    results = []
    for terraform_file in terraform_files_list:
        try:
            result = subprocess.run(['terraform', 'validate', terraform_file],
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                cli_status = "[v] PASS"
            else:
                cli_status = f"[X] FAIL: {result.stderr.strip()}"
        except FileNotFoundError:
            cli_status = "[!] Terraform CLI not found"
        except subprocess.TimeoutExpired:
            cli_status = "[X] Timeout"
        
        print(f"CLI {terraform_file}: {cli_status}")
        results.append({'file': terraform_file, 'cli_status': cli_status})
    
    return results
    
def terraform_parse():
    results = []
    for terraform_file in terraform_files_list:
        try:
            with open (terraform_file, 'r') as file:
                dict = hcl2.load(file)
            status = "[v] PASS"

        except Exception as e:
            status = f'[X] FAIL: {e}'
            
        print (f"{terraform_file}: {status}")
        results.append({'file': terraform_file, 'status': status})
    return results

list_terraform_files()
print(f"Found {len(terraform_files_list)} files .tf")
print("TERRAFORM CLI ERRORS:")
terraform_validate()
print("HCL2 SYNTAX ERROR:")
terraform_parse()