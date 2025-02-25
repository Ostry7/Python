import paramiko
import os
from datetime import datetime 
import subprocess

def execute_ssh_command(hostname, user, command,key_path):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, username=user, key_filename=key_path)
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()
        client.close()
        return output, error  
    except Exception as e:
        print(f'Error during connection to {hostname}: {e}')
        return "", str(e) 


def generate_new_key(username):
    key_dir = os.path.expanduser(f'~/.ssh/{username}_keys')
    os.makedirs(key_dir, exist_ok=True)
    private_key_path = os.path.join(key_dir, f'id_ed25519_{datetime.now().strftime("%Y-%m-%d")}')
    public_key_path = private_key_path + '.pub'
    print(public_key_path)

    try:
        subprocess.run(
            ["ssh-keygen", "-t", "ed25519", "-N", "", "-f", private_key_path],
            check=True 
        )
        print(f'SSH key has been generated: {private_key_path}')
        return private_key_path, public_key_path
    except subprocess.CalledProcessError as e:
        print(f'Error generating SSH key: {e}')
        return "", ""



def send_ssh_key(user, username, host,public_key_path ):
    try:
        print(public_key_path)
        with open(public_key_path, 'r') as key_file:
            public_key = key_file.read().strip()

        
        command = f'echo "{public_key}" | sudo tee -a /home/{username}/.ssh/authorized_keys &&  sudo chmod 600 /home/{username}/.ssh/authorized_keys'
        key_path = 'C:/Users/ostro/.ssh/id_ed25519'
        output, error = execute_ssh_command(host, user, command, key_path)
        if error:
            print(f'Cannot generate key for {host}: {error}')
        else:
            print('Successfully generated key!')
    except FileNotFoundError:
        print('Cannot find public key')


def main():
    action = input('Select: [1]Add new key ')

    if action not in ['1']:
        print('Select correct action')
        return

    username = input('Enter the user to whom we will generate the key: ')
    host = '192.168.5.100'  # local UBUNTU
    user = 'adminek'

    if action == '1':
        private_key_path, public_key_path = generate_new_key(username)
        if not private_key_path or not public_key_path:
            print('Failed to generate SSH key pair.')
            return
        key_path = 'C:/Users/ostro/.ssh/id_ed25519'
        send_ssh_key(user,username,host, public_key_path)



if __name__ == '__main__':
    main()
