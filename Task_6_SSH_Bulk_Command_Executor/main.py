import paramiko

# host config
HOST_NAME = "192.168.68.240" #debian
USER_NAME = "USER"
PASSWORD = "PASSWORD"
#PRIVATE_KEY_FILE = '/some/file/path/private_key.txt'
PORT = 22

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=HOST_NAME, port=PORT, username=USER_NAME, password=PASSWORD)

command = "ls -l"
stdin, stdout, stderr = client.exec_command(command)
print(stdout.read())
