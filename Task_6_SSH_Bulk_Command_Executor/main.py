import paramiko
import yaml

with open("bulk.yaml", 'r') as f:
    config = yaml.safe_load(f)
hosts = config["hosts"]
commands = config["commands"]

def ssh_connect(IP_ADDRESS,HOST_NAME,PORT,USER_NAME,PASSWORD):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=IP_ADDRESS, port=PORT, username=USER_NAME,  password=PASSWORD)
        print(f"SUCCESSFULLY CONNECTED TO THE {HOST_NAME} !")
        exec_commands(client, HOST_NAME)
        client.close()

    except Exception as e:
        print(f"Cannot connect to the {HOST_NAME}: {e}")

def exec_commands(client, HOST_NAME):
    try:
        for command in commands:
            stdin, stdout, stderr = client.exec_command(command)
            output = stdout.read().decode()
            error = stderr.read().decode()
            print(f"[{HOST_NAME}] $ {command}")
            print(output if output else error)
    except Exception as e:
        print(f"Cannot exec commands on {HOST_NAME}: {e}")
    except:
        print(f"Cannot exec commands!")

for host in hosts:
    ssh_connect(
        host["ip"],
        host["name"],
        host["port"],
        host["user"],
        host["password"]
    )



    