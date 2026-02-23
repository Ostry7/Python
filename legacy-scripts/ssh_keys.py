import paramiko
import os
from datetime import datetime
import subprocess

def get_key_paths(username):
    key_dir = os.path.expanduser(f'~/.ssh/{username}_keys')
    private_key_path = os.path.join(key_dir, f'id_ed25519_{datetime.now().strftime("%Y-%m-%d")}')
    public_key_path = private_key_path + '.pub'
    return private_key_path, public_key_path


def execute_ssh_command(hostname, user, command, key_path):
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
    private_key_path, public_key_path = get_key_paths(username)
    os.makedirs(os.path.dirname(private_key_path), exist_ok=True)

    try:
        subprocess.run(["ssh-keygen", "-t", "ed25519", "-N", "", "-f", private_key_path], check=True)
        print(f'SSH key has been generated: {private_key_path}')
        return private_key_path, public_key_path
    except subprocess.CalledProcessError as e:
        print(f'Error generating SSH key: {e}')
        return "", ""


def send_ssh_key(user, username, host, public_key_path, key_path):
    try:
        with open(public_key_path, 'r') as key_file:
            public_key = key_file.read().strip()

        command = (
            f'sudo -S mkdir -p /home/{username}/.ssh && '
            f'sudo chmod 700 /home/{username}/.ssh && '
            f'echo "{public_key}" | sudo tee -a /home/{username}/.ssh/authorized_keys && '
            f'sudo chmod 600 /home/{username}/.ssh/authorized_keys && '
            f'sudo chown -R {username}:{username} /home/{username}/.ssh'
        )

        output, error = execute_ssh_command(host, user, command, key_path)
        if error:
            print(f'Cannot generate key for {host}: {error}')
        else:
            print('Successfully generated key!')
    except FileNotFoundError:
        print('Cannot find public key')


def delete_old_keys(user, username, host, key_path):
    private_key_path, _ = get_key_paths(username)
    public_key_path, _ = get_key_paths(username)

    try:
        # Usuń klucz z serwera
        command = f'sudo -S rm -f /home/{username}/.ssh/authorized_keys'
        output, error = execute_ssh_command(host, user, command, key_path)
        if error:
            print(f'Cannot remove old keys for {host}: {error}')
        else:
            print('Successfully removed old SSH keys!')

        # Usuń lokalny klucz prywatny
        if os.path.exists(private_key_path):
            os.remove(private_key_path)
            os.remove(public_key_path)
            print(f'Successfully removed private key: {private_key_path}')
        else:
            print(f'Private key not found: {private_key_path}')
    except Exception as e:
        print(f'Error while removing old SSH keys: {e}')

def reroll_keys(user, username, host, key_path):
    print(f"\n--- Rerolling SSH keys for {username} on {host} ---")
    delete_old_keys(user, username, host, key_path)
    private_key_path, public_key_path = generate_new_key(username)
    if private_key_path and public_key_path:
        send_ssh_key(user, username, host, public_key_path, key_path)
        print('Successfully rerolled SSH keys!')
    else:
        print('Failed to reroll SSH keys.')



def main():
    action = input('Select: \n [1] Add new key \n [2] Delete old keys \n [3] Reroll keys\n> ')

    if action not in ['1', '2', '3']:
        print('Select correct action.')
        return

    username = input('Enter the user to whom we will generate the key: ')
    host = 'ip_address'  # lokalna maszyna Ubuntu
    user = 'linux_user'
    key_path = 'path to private key'

    if action == '1':
        private_key_path, public_key_path = generate_new_key(username)
        if private_key_path and public_key_path:
            send_ssh_key(user, username, host, public_key_path, key_path)
        else:
            print('Failed to generate SSH key pair.')

    elif action == '2':
        delete_old_keys(user, username, host, key_path)
    elif action == '3':
        reroll_keys(user, username, host, key_path)


if __name__ == '__main__':
    main()
