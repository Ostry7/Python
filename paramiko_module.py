import paramiko
#WSL local IP address 



def connect_to_server(host, username, password=None, key_file=None):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if key_file:
            ssh_client.connect(host, username=username, key_filename=key_file)
        else:
            ssh_client.connect(host, username=username, password=password)
        print (f'Successfully connected to {host}')
        return ssh_client
    except Exception as e:
        print(f"Error connection: {e}")
        return None

def exec_command(ssh_client, command):
    try:
        stdin, stdout, stderr = ssh_client.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()
        if error:
            print(f"Error: {error}")
        return output
    except Exception as e:
        print(f"Cannot execute command: {e}")
        return None    

host = 'IP_ADDRESS'
username = 'USER'
password = 'PASSWORD!'
command = 'COMMAND'

ssh_client = connect_to_server(host, username, password)
if ssh_client:
    output = exec_command(ssh_client, command)
    print(f"Output of {command}: {output}")
    ssh_client.close()