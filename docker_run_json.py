import docker
import json
import time
import csv

client = docker.from_env()  #Connect to Docker using the default socket or the configuration in your environment
csv_file = 'container_stats.csv'

def launch_containers(filename, existing_containers_info):
    with open(filename) as f:
        config = json.load(f)

    all_container_list()  
    for container_name, container_config in config.items():
        print (f'Launching ---> {container_name}...')
        if container_name not in [c['name'] for c in existing_containers_info]:
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
    existing_containers_info = []
    for container in client.containers.list(all=True):     #all=True -> for all containers
        existing_containers_info.append({
            'name': container.name,
            'id': container.short_id,
            'status': container.status
        })
    return existing_containers_info

def stop_containers():
    container_list = client.containers.list()
    for container in container_list:
        print(f'Stopping container ---> {container.id}')
        container.stop()

def delete_unused_containers():
    containers = client.containers.list(all=True)
    unused_containers = [container for container in containers if container.status in ['exited', 'created']]
    if not unused_containers:
            print('There is no containers in exited or created state')
    for container in unused_containers:
            try:
                container.remove()
                print(f'Removing unused container ---> {container.name}, ID: {container.id}')
            except Exception as e:
                print (f'Error while removing {container.name}: {e}')

def containers_monitor(interval=5):

    try:
        while True:
            print('Current container status')
            containers = client.containers.list(all=True)

            if not containers:
                print('There is no running containers')
            
            with open(csv_file, mode='a', newline='') as file:
                writer = csv.writer(file)

                for container in containers:
                    stats = container.stats(stream=False)     #get statistics
                    #CPU Calculation:
                    cpu_delta = stats["cpu_stats"]["cpu_usage"]["total_usage"] - stats["precpu_stats"]["cpu_usage"]["total_usage"]
                    system_delta = stats["cpu_stats"]["system_cpu_usage"] - stats["precpu_stats"]["system_cpu_usage"]
                    cpu_usage = (cpu_delta / system_delta) * len(stats["cpu_stats"]["cpu_usage"]["percpu_usage"]) * 100 if system_delta > 0 else 0

                    # Memory Usage calculation:
                    mem_usage = stats["memory_stats"]["usage"] / (1024 * 1024)  # MB
                    mem_limit = stats["memory_stats"]["limit"] / (1024 * 1024)  # MB
                    mem_percentage = (mem_usage / mem_limit) * 100 if mem_limit > 0 else 0

                    print(f'Container {container.name} | Status: {container.status}')
                    print(f'CPU: {cpu_usage:.2f}% | RAM: {mem_usage:.2f}MB / {mem_limit:.2f}MB ({mem_percentage:.2f}%)')

                    writer.writerow([
                        container.name,
                        round(cpu_usage, 2),
                        round(mem_percentage, 2)
                    ])
        time.sleep(interval)
    except KeyboardInterrupt:
        print ('Stopping monitoring...')
    finally:
        print (f'Monitoring data saved in {csv_file}')

#existing_containers_info = all_container_list()
#delete_unused_containers()
#launch_containers('docker_config.json', existing_containers_info)     
#stop_containers()
#containers_monitor()

