import docker
import time

client = docker.from_env()
containers = client.containers.list()



def collect_cpu():
    for container in containers:
        for stats in container.stats(stream=True, decode=True):
            stats = container.stats(stream=False)         
            cpu_delta = stats["cpu_stats"]["cpu_usage"]["total_usage"] - \
                       stats["precpu_stats"]["cpu_usage"]["total_usage"]
            system_delta = stats["cpu_stats"]["system_cpu_usage"] - \
                          stats["precpu_stats"]["system_cpu_usage"]

            cpu_percent = (cpu_delta / system_delta) * 100.0 if system_delta > 0 else 0
            mem_mb = stats['memory_stats']['usage'] / 1024 / 1024
            container_name = container.name
            print(f"====={container_name} =====")
            print(f"CPU: {cpu_percent:.1f}% | MEM: {mem_mb:.1f}MB")
            print("---")
            time.sleep(1)
collect_cpu()
