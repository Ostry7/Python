#idea:
#create new ssh key for user and copy it to ~/.ssh/authorized_keys 
#delete ssh key based on path
#rotate: delete old ssh key and generete new one

#generate key
#sudo mkdir -p /home/USERNAME/.ssh
#sudo chmod 700 /home/USERNAME/.ssh
#sudo touch /home/USERNAME/.ssh/authorized_keys
#sudo chmod 600 /home/USERNAME/.ssh/authorized_keys
#cat ~/key.pub >> ~USERNAME/.ssh/authorized_keys
#sudo chown -R USERNAME:USERNAME /home/USERNAME/.ssh

import paramiko

#username = input('Enter username')
hostname = '192.168.5.100'  #local CENTOS
keypair= 'C:/Users/ostro/.ssh/id_ed25519' #key filename included

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname, key_filename=keypair)
stdin, stdout, stderr = client.exec_command("sudo mkdir /home/jas/")

print(stdout.read().decode())
stdout.close()
stdin.close()
client.close()


#def createkey():
#    command = 
