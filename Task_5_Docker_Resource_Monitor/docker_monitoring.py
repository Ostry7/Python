import docker
import time
import json
from datetime import datetime

client = docker.from_env()
containers = client.containers.list(all=False)
stats_list = []



def collect_cpu():
    for container in containers: 
        stats = container.stats(stream=False)         
        cpu_delta = stats["cpu_stats"]["cpu_usage"]["total_usage"] - \
                   stats["precpu_stats"]["cpu_usage"]["total_usage"]
        system_delta = stats["cpu_stats"]["system_cpu_usage"] - \
                      stats["precpu_stats"]["system_cpu_usage"]
        cpu_percent = (cpu_delta / system_delta) * 100.0 if system_delta > 0 else 0
        mem_mb = stats['memory_stats']['usage'] / 1024 / 1024
        stats_list.append({
            'timestamp': datetime.now().isoformat(),
            'container': container.name,
            'cpu': f"{cpu_percent:.1f}",
            'memory': f"{mem_mb:.1f}"
        })
        
        with open ('stats.json', 'w') as f:
            json.dump(stats_list, f, indent=2)
        time.sleep(1)
collect_cpu()
