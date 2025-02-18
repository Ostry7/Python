import docker
import json



def launch_containers(filename):
    with open(filename) as f:
        config = json.load(f)
        print (type(config))

    client = docker.from_env()  #Connect to Docker using the default socket or the configuration in your environment

    for container_name, container_config in config.items():
        print (f'Launching {container_name}...')
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

launch_containers('docker_config.json')
