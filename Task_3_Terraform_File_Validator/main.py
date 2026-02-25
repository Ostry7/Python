import os
import hcl2

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


def terraform_parse():
    results = []
    for terraform_files in terraform_files_list:
        try:
            with open (terraform_files, 'r') as file:
                dict = hcl2.load(file)
            status = "[v] PASS"

        except Exception as e:
            status = f'[X] FAIL: {e}'
            
        print (f"{terraform_files}: {status}")
        results.append({'file': terraform_files, 'status': status})
    return results

list_terraform_files()
print(f"Found {len(terraform_files_list)} files .tf")
terraform_parse()