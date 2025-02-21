#idea:
#create new ssh key for user and copy it to ~/.ssh/authorized_keys 
#delete ssh key based on path
#rotate: delete old ssh key and generete new one

import paramiko
import os
import subprocess
import logging
from datetime import datetime

# Konfiguracja logowania
log_file = "ssh_key_management.log"
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename=log_file)

def execute_ssh_command(host, user, command):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=user)
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()
        client.close()
        return output, error
    except Exception as e:
        logging.error(f"Błąd połączenia z {host}: {e}")
        return None, str(e)