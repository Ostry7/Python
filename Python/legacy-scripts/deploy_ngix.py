import paramiko

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

def exec_command(ssh_client, command):
    try:
        stdin, stdout, stderr = ssh_client.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()
        if error:
            print(f"Error: {error}")
        return output, error  # Ensure we always return both output and error
    except Exception as e:
        print(f"Cannot execute command: {e}")
        return None, str(e)  # Ensure we return both output and error

def get_linux_version(ssh_client):
    command = "cat /etc/os-release | grep PRETTY_NAME"
    output, error = exec_command(ssh_client, command)
    if output:
        return output.split("=")[1].strip().strip('"')
    return "Unknown OS"

def ngix_install_ubuntu(ssh_client):
    check_nginx_status_cmd = 'systemctl is-active --quiet nginx'
    stdin, stdout, stderr = ssh_client.exec_command(check_nginx_status_cmd)
    if stdout.channel.recv_exit_status() == 0: #if nginx is up
        print("Nginx is already running. Skipping installation.")
        return 
    
    commands = [
        'sudo apt update -y',
        'sudo apt install nginx -y',
        'sudo systemctl start nginx',
        'sudo systemctl enable nginx'
    ]
    for cmd in commands:
        print(f"Executing: {cmd}")
        exec_command(ssh_client, cmd)
    
    print("Nginx installation complete!")

def ngix_install_centos(ssh_client):
    check_nginx_status_cmd = 'systemctl is-active --quiet nginx'
    stdin, stdout, stderr = ssh_client.exec_command(check_nginx_status_cmd)
    if stdout.channel.recv_exit_status() == 0: #if nginx is up
        print("Nginx is already running. Skipping installation.")
        return 
    
    commands = [
        'sudo yum update -y',
        'sudo yum install nginx -y',
        'sudo systemctl start nginx',
        'sudo systemctl enable nginx'
    ]
    for cmd in commands:
        print(f"Executing: {cmd}")
        exec_command(ssh_client, cmd)
    
    print("Nginx installation complete!")

def start_fastapi_app(ssh_client):
    commands = [
        "echo 'from fastapi import FastAPI\napp = FastAPI()\n@app.get(\"/\")\ndef hello():\n    return {\"message\": \"Hello, World from FastAPI!\"}\nif __name__ == \"__main__\":\n    import uvicorn\n    uvicorn.run(app, host=\"0.0.0.0\", port=8000)' | sudo tee /home/{user}/app.py",
        'sudo ufw allow 8000/tcp',
        'nohup /usr/bin/python3 /home/{user}/app.py > /home/{user}/app.log 2>&1 &'
    ]
    for cmd in commands:
        print(f"Executing: {cmd}")
        exec_command(ssh_client, cmd)
    print("FastAPI app is running on port 8000!")

def main():
    host = "IP_ADDRESS"
    username = "USER"
    key_file = "KEY_FILE_DIR"

    ssh_client = connect_to_server(host, username, key_file=key_file)
    if ssh_client:
        os_type = get_linux_version(ssh_client)
        print(f"Detected OS: {os_type}")
        if 'Ubuntu' in os_type:
            ngix_install_ubuntu(ssh_client)
        elif 'CentOS' in os_type:
            ngix_install_centos(ssh_client)
        start_fastapi_app(ssh_client)
        ssh_client.close()

if __name__ == "__main__":
    main()
