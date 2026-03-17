import paramiko
import json
#useradd -m -p $(openssl passwd -1 $PASS) $USER

servers = ['192.168.5.100']  

with open('bulk_user_create.json', 'r') as file:
    users = json.load(file)


def connect_to_server(host, username, password=None, key_file=None):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if key_file:
            ssh_client.connect(host, username=username, key_filename=key_file)
        else:
            ssh_client.connect(host, username=username, password=password)
        print(f'Successfully connected to {host}')
        return ssh_client
    except Exception as e:
        print(f"Error connecting to {host}: {e}")
        return None


def create_user(ssh_client, username, password):
    try:
        command = f"sudo useradd -m -p $(openssl passwd -1 {password}) {username}"
        stdin, stdout, stderr = ssh_client.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()
        
        if error:
            print(f"Error creating user {username}: {error}")
        else:
            print(f"User {username} created successfully.")
        return output
    except Exception as e:
        print(f"Cannot execute command: {e}")
        return None

for server in servers:
    ssh_client = connect_to_server(server, 'user', password='password')  
    if ssh_client:
        for user in users:
            create_user(ssh_client, user['username'], user['password'])
        ssh_client.close()