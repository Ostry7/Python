import paramiko
import os
from datetime import datetime 
import subprocess

#username = input('Enter username')

keypair= 'C:/Users/ostro/.ssh/id_ed25519' #key filename included

#client = paramiko.SSHClient()
#client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#client.connect(hostname, username='ostry',key_filename=keypair)
#stdin, stdout, stderr = client.exec_command("whoami")

#print(stdout.read().decode())
#stdout.close()
#stdin.close()
#client.close()


def execute_ssh_command(hostname, username, command):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, username=username)
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()
        client.close()
        return output, error  # Zawsze zwracamy output i error
    except Exception as e:
        print(f'Error during connection to {hostname}: {e}')
        return "", str(e)  # Zwróć dwie wartości: pusty output i błąd


def generate_new_key(username):
    key_dir = os.path.expanduser(f'~/.ssh/{username}_keys')
    os.makedirs(key_dir, exist_ok=True)
    private_key_path = os.path.join(key_dir, f'id_rsa_{datetime.now().strftime("%Y-%m-%d")}')
    public_key_path = private_key_path + '.pub'

    try:
        subprocess.run(
            ["ssh-keygen", "-t", "rsa", "-b", "4096", "-N", "", "-f", private_key_path],
            check=True  # check=True, aby zgłosić wyjątek w przypadku błędu
        )
        print(f'SSH key has been generated: {private_key_path}')
        return private_key_path, public_key_path
    except subprocess.CalledProcessError as e:
        print(f'Error generating SSH key: {e}')
        return "", ""  # Zwróć pustą ścieżkę w przypadku błędu


def send_ssh_key(user, host, key_path):
    try:
        with open(key_path, 'r') as key_file:
            public_key = key_file.read().strip()  # strip to remove all spaces of the string
        command = f'echo "{public_key}" >> ~/.ssh/authorized_keys'
        output, error = execute_ssh_command(host, user, command)
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

    username = input('Enter user which can generate keys in Linux server: ')
    host = '192.168.5.100'  # local CENTOS
    user = input('Enter user for key generate')

    if action == '1':
        private_key_path, public_key_path = generate_new_key(username)
        if not private_key_path or not public_key_path:
            print('Failed to generate SSH key pair.')
            return
        send_ssh_key(username, host, public_key_path)



if __name__ == '__main__':
    main()
