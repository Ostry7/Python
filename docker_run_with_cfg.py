import docker
import json

client = docker.from_env()  #Connect to Docker using the default socket or the configuration in your environment

def launch_containers(filename, existing_containers):
    with open(filename) as f:
        config = json.load(f)
    
    all_container_list()  
    for container_name, container_config in config.items():
        print (f'Launching ---> {container_name}...')
        if container_name not in existing_containers:
            try:
                client.containers.run(
                    image=container_config.get('image'),
                    detach=True,
                    ports=container_config.get('ports'),
                    volumes=container_config.get('volumes'),
                    environment=container_config.get('environment'),
                    name=container_name
                )
                print(f'Successfully launch {container_name}')
            except Exception as e:
                print(f'Error: {e}')
        else:
            print(f'Container {container_name} already exists, skipping creation...')

def all_container_list():
    existing_containers = []
    for container in client.containers.list(all=True):     #all=True -> for all containers
        existing_containers.append(container.name)
    return existing_containers

def stop_containers():
    container_list = client.containers.list()
    for container in container_list:
        print(f'Stopping container ---> {container.id}')
        container.stop()


existing_containers = all_container_list()
launch_containers('docker_config.json', existing_containers)     
#stop_containers()
#running_container_list()
